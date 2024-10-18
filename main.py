# Codebase modules
import database
import transcript_utils

# Test timestamps
def main():

    conn = database.connect_db()
    database.create_tables(conn)

    # Dummy test data -> insert video_IDs
    test_video_ids = []
    test_video_ids_2 = []

    for test_id in test_video_ids_2:
        video_data = transcript_utils.get_video_transcript(test_id)

        # transcript_utils.write_transcript_to_file(video_data["grouped_transcripts"], "graham-hancock")

        database.insert_video_data(conn, video_data)
        print("*****************")


    rows = database.get_chunked_transcripts(conn, "q8VePUwjB9Y")
    for row in rows:
        print(row[:100])

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