# Codebase modules
import database
import transcript_utils
import channel_utils

# Test timestamps
def main():

    conn = database.connect_db()
    database.create_tables(conn)

    # List of new video_ids to be added to the collection
    test_video_ids = []

    # Prompt for a youtube video URL (the podcast that we want to get the transcripts from)
    user_input = input("Please enter a Youtube URL to a video that you want to transcript or press ENTER to exit: ")
    while (user_input != ""):
    
        # Get the ID of the related video from the URL through parsing
        new_video_id = channel_utils.url_to_video_id(user_input)
        if new_video_id == None:
            print("No video_ID found - please try again")
        else:
            print(f"New video id is: {new_video_id}")
            test_video_ids.append(new_video_id)

        user_input = input("Please enter a Youtube URL to a video that you want to transcript or press ENTER to exit: ")


    # Get the transcripts from the new videos and add them to the collection
    for test_id in test_video_ids:
        video_data = transcript_utils.get_video_transcript(test_id)
        database.insert_video_data(conn, video_data)
        print("*****************")

    print("--- Testing label insertion: ---")
    cur = conn.cursor()
    cur.execute("SELECT timestamp_label FROM timestamps")
    rows = cur.fetchall()
    for row in rows:
        print(row)


    '''
    print("---- \n\nTest results for correct insertion in database\n----")
    print("---- Test videos table ----")
    cur = conn.cursor()
    cur.execute("SELECT * FROM videos")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    print()
    print("---- Test timestamps table ----")
    cur.execute("SELECT * FROM timestamps")
    rows = cur.fetchall()
    for row in rows:
        print(row[3])
        print(row[4][:100])
        print(row)

    print("---- Test transcripts table -----")
    cur.execute("SELECT * FROM transcripts")
    rows = cur.fetchall()
    for row in rows:
        print(row[2][:100])
    conn.close()
    '''



if __name__ == "__main__":
    main()