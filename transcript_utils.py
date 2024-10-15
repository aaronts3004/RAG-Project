
''' 
    Module responsible for transcript processing and chunking of the transcript text
    based on the single timestamps that were scraped from the youtube video
'''

import re
from youtube_transcript_api import YouTubeTranscriptApi
import googleapiclient.errors
import youtube_api

# Convert a single timestamp (str) into time seconds format (int)
def timestamp_to_seconds(timestamp_str):
    parts = timestamp_str.split(':')        # each part is either hh, mm, or ss
    parts = [int(part) for part in parts]   # convert each hh, mm or ss into integer
    if len(parts) == 3:
        # Format is HH:MM:SS
        hours, minutes, seconds = parts
    elif len(parts) == 2:
        # Format is MM:SS
        hours = 0
        minutes, seconds = parts
    else:
        # Invalid format
        print("****       !!! Timestamp could not be converted into desired integer format !!!      ****")
        return None
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds


'''
    Function to process the raw transcript from the YoutubeTranscriptApi
    The YoutubeTranscriptApi returns the transcript as a list of text chunks (stored as dicts)
    e.g. [
        {'text': '- The following is a conversation\n with...,', 'start': 0.12, 'duration': 3.39}, 
        {'text': 'his second time on this,\n" Podcast."', 'start': 3.51, 'duration': 3.867},
        ...
    ]
    This can be useful, but the duration of the chunks is way too short.
    Therefore, chunks must be grouped together so that they match to a corresponding entry in timestamps table
'''
def process_transcript_chunks(chunk_list, timestamps_list):
    # Iterate over the list of timestamps, convert the 'timestamp' component of the dict 
    # add the representation of the timestamp in seconds to the dict
    for ts in timestamps_list:
        ts_seconds = timestamp_to_seconds(ts['timestamp'])
        ts['start_time'] = ts_seconds  # Add a 'start_time' in seconds

    # Ensure timestamps are sorted by 'start_time'
    timestamps_list = sorted(timestamps_list, key=lambda x: x['start_time'])

    # Create a list of intervals that contain:
    # * The label for the current timestamp
    # * Start and end times (in seconds) for each label
    intervals = []
    for i in range(len(timestamps_list)):
        start_time = timestamps_list[i]['start_time']
        label = timestamps_list[i]['text']  # Label from the description
        if i + 1 < len(timestamps_list):
            end_time = timestamps_list[i + 1]['start_time']
        else:
            end_time = None  # Last interval; will handle later
        intervals.append({
            'label': label,
            'start_time': start_time,
            'end_time': end_time
        })

    # print("---- Timestamps: ----")
    # print(timestamps_list)
    # print()
    # print("---- Intervals ----")
    # print(intervals)

    # Start processing the text chunks from the transcript to assign each chunk to a label+timestamp
    # The goal is to group the small text chunks into larger chunks, so that each large chunk
    # maps to a large timestamp. Prepare a structure to hold the grouped transcripts
    grouped_transcripts = []

    # Index to keep track of which interval we're in
    interval_index = 0
    current_interval = intervals[interval_index]
    current_group = {
        'label': current_interval['label'],
        'start_time': current_interval['start_time'],
        'end_time': current_interval['end_time'],
        'text': ''
    }
    grouped_transcripts.append(current_group)

    for chunk in chunk_list:
        chunk_start = chunk['start']
        # Check if the chunk belongs to the current interval
        while current_interval['end_time'] is not None and chunk_start >= current_interval['end_time']:
            # Move to the next interval
            interval_index += 1
            if interval_index < len(intervals):
                current_interval = intervals[interval_index]
                current_group = {
                    'label': current_interval['label'],
                    'start_time': current_interval['start_time'],
                    'end_time': current_interval['end_time'],
                    'text': ''
                }
                grouped_transcripts.append(current_group)
            else:
                # No more intervals; exit loop
                break
            if interval_index >= len(intervals):
                break  # All intervals are processed

        # Append the chunk's text to the current group's text
        current_group['text'] += ' ' + chunk['text']

    return grouped_transcripts


# Write the timestamped chunks from the transcript to 'filename'
def write_transcript_to_file(grouped_transcripts, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for group in grouped_transcripts:
                start_time = group['start_time']
                text = group['text']

                # Format the start_time into HH:MM:SS
                hours = int(start_time // 3600)
                minutes = int((start_time % 3600) // 60)
                seconds = int(start_time % 60)
                timestamp_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

                # Write to the file
                f.write(f"Timestamp: {timestamp_formatted}\n")
                f.write(f"Text:{text}\n\n")
        print(f"Transcript has been written to file")
    except Exception as e:
        print(f"Error writing to file: {e}")
        return
    

# Function to get the transcript for an input video ID
def get_video_transcript(video_id):

    youtube = youtube_api.get_youtube_client()

    # Use the YouTubeTranscriptApi to fetch transcript
    transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )

    try: 
        response = request.execute()
        snippet = response["items"][0]["snippet"]       # The 'snippet' will contain the relevant fields
        
        title = snippet.get("title", "Unknown Title")
        desc = snippet.get("description","Empty Description")
        channel_name = snippet.get("channelTitle", "Unknown Channel")

        # Regular expression to capture timestamps from the description (HH:MM:SS or MM:SS format)
        timestamp_pattern = r'\(?(\d{1,2}:\d{2}(?::\d{2})?)\)?\s+(.*)'

        # Use regex to find all matching timestamps and their descriptions
        matches = re.findall(timestamp_pattern, desc)

        # Create a list to store parsed timestamps and their descriptions
        timestamps = []

        # Loop through matches and store the timestamp with the associated label
        for match in matches:
            timestamps.append({
                "timestamp": match[0],
                "text": match[1]
            })
        
        grouped_transcripts = process_transcript_chunks(transcript_text, timestamps)
    
        # write_transcript_to_file(grouped_transcripts, "test_file.txt")
        
        # Write all the data to the database
        video_data = {
            "video_id": video_id,
            "title": title,
            "description": desc,
            "channel_name": channel_name,
            "timestamps_array": timestamps,
            "grouped_transcripts": grouped_transcripts
        }

        return video_data

    except googleapiclient.errors.HttpError as e:
        print("An error occurred while executing the API request:")
        print(e)