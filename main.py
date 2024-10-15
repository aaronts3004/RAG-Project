# Native modules

import database
import sqlite3
import channel_utils
import transcript_utils


# Function to save transcript to file
def save_transcript(transcript, filename):
    # Save the transcript string to a text file
    print()


# Main function
def main_functionality():
    channel_handle = input("Enter YouTuber's handle: ")
    
    # Convert handle to channel ID 
    channel_id = channel_utils.handle_to_channel_id(channel_handle)
    
    video_ids = channel_utils.get_channel_videos(channel_id)
    print("--- End of fetching video IDs ---")

    
    for video_id in video_ids:
        transcript = transcript_utils.get_video_transcript(video_id)
        filename = f"{video_id}_transcript.txt"
        save_transcript(transcript, filename)

# Test timestamps
def main():
    cur_id = "uvFtyDy_Bt0"
    video_data = transcript_utils.get_video_transcript(cur_id)
    print(video_data["timestamps_array"])


def test_database():
    cur_id = "uvFtyDy_Bt0"

    # Connect to the database
    # conn = database.connect_db()

    # Create the necessary tables
    # database.create_tables(conn)

    video_data = transcript_utils.get_video_transcript(cur_id)
    timestamps_array = video_data["timestamps_array"]

    # print("try insertion")
    # print(f"Type of channel_title: {type(video_data['channel_name'])} - title: {video_data['channel_name']}")
    # print(f"Type of channel_description: {type(video_data['description'])} - title: {video_data['description']}")
    # print("--------------------------------------------------")

    # print(f"ype of transcript: {[type(video_data["transcript"])]}")
    # for x in range(30):
        # print(video_data["transcript"][x]["text"])


    try:
        # database.insert_transcript(conn, cur_id, video_data)
        # database.insert_timestamps(conn, cur_id, timestamps_array)
        print("finished inserting into database")
    except sqlite3.Error as e:
        print(e)
    except Exception as e:
        print(e)
        return 
    
    print(" ")
    print("---  successful insertion: test transcripts ---")
    # test correct insertion
    cur = conn.cursor()
    cur.execute("select * from transcripts")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    print(" ")
    print("--- test timestamps ---")
    cur.execute("select * from timestamps")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    
    print("closing db connection")
    conn.close()

    
def another_main():
    conn = database.connect_db()
    cur = conn.cursor()
    cur.execute()


if __name__ == "__main__":
    main()