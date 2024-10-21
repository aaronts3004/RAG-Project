''' 
    Handles all the channel-related code to retrieve 
    channel-ID, video-IDs, video-transcripts, etc...
'''

import time
import googleapiclient.errors
from youtube_api import get_youtube_client  # Import the centralized YouTube API client
import re


# Function to get the channelID from a @handle
def handle_to_channel_id(username):
    youtube = get_youtube_client()
    request = youtube.channels().list(
        part="id, contentDetails",
        forHandle=username
    )

    try:
        response = request.execute()
        print("--- Executed API request and printing response --- ")
        print(response)
        print("--- End of API request response to get ID --- ")
        if 'items' in response and len(response['items']) > 0:
            channel_id = response['items'][0]['id']
            print("--- Channel ID: " + channel_id + " ---")
            return channel_id
        else:
            print(f"No channel found for handle: {username}")
            return None

    except googleapiclient.errors.HttpError as e:
        print("An error occurred while executing the API request:")
        print(e)
        return None


# Function to get video IDs of all the uploaded videos from the Channel ID
def get_channel_videos(channel_id):
    youtube = get_youtube_client()
    
    video_ids = set()
    next_page_token = None
    
    while True:
        request = youtube.search().list(
            part="id",
            channelId=channel_id,
            type="video",
            maxResults=50,
            pageToken=next_page_token,
            order="date"
        )
        
        try:
            response = request.execute()
            
            for item in response['items']:
                video_ids.add(item['id']['videoId'])
            
            next_page_token = response.get('nextPageToken')
            print(f"Fetched {len(video_ids)} videos so far...")
            # Add a delay to avoid hitting API rate limits
            time.sleep(1)
            
            if not next_page_token:
                break
        
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred while fetching video IDs: {e}")
            break

    print(f"Total videos fetched: {len(video_ids)}")
    return video_ids

def url_to_video_id(url_string):
    match = re.search(r"v=([a-zA-Z0-9_-]{11})", url_string)
    if match:
        return match.group(1)
    else:
        return None


'''
# Retrieve the ID of the playlist that contains the 'podcast' uploads
def get_podcasts_playlist_ID(channel_ID):
    youtube = get_youtube_client()
    
    video_ids = set()

    try: 
        channel_response = youtube.playlists().list(
            part='snippet',
            channelId = channel_ID
        ).execute()
    except googleapiclient.errors.HttpError as e:
        print("An error occurred while executing the API request:")
        print(e)

    print(channel_response['items'])
'''

