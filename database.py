import sqlite3

# Estabilish database connection, create database if not existent
def connect_db():
    """ create the SQLite database connection """
    conn = None
    try:
        conn = sqlite3.connect("transcript_database.db")
        print(sqlite3.sqlite_version)
        if conn:
            return conn
    except sqlite3.Error as e:
        print(e)

# Table schema definition
def create_tables(conn):
    sql_statements = [ 
        """CREATE TABLE IF NOT EXISTS videos (
            video_id TEXT PRIMARY KEY,
            title TEXT,
            channel TEXT,
            description TEXT
        );""",

        """CREATE TABLE IF NOT EXISTS transcripts (
            video_id TEXT PRIMARY KEY,
            video_title TEXT,
            video_transcript TEXT,
            FOREIGN KEY (video_id) REFERENCES videos(video_id)
        );""",
        
        """CREATE TABLE IF NOT EXISTS timestamps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT,
            timestamp_Time TEXT,
            timestamp_Label TEXT,
            transcript_Chunk TEXT,
            FOREIGN KEY (video_id) REFERENCES videos(video_id)
        );"""
        
    ]

    # create a database connection
    try:
        cursor = conn.cursor()
        count = 0
        for statement in sql_statements:
            cursor.execute(statement)
            print(f"executed sql {count}")
            count += 1
            
        conn.commit()
    except sqlite3.Error as e:
        print(e)


# Function to insert timestamps with the corresponding textual transcript chunks
def insert_transcript_chunks(conn, video_id, grouped_transcripts_array):
    cursor = conn.cursor()

    sql_statement = '''
        INSERT INTO timestamps (video_id, timestamp_Label, transcript_Chunk)
        VALUES (?, ?, ?)
    '''

    for entry in grouped_transcripts_array:
        cursor.execute(sql_statement, (video_id, entry["label"], entry["text"]))

    conn.commit()
    print(f"Successfully inserted transcript chunks of video_ID: {video_id}")


def insert_single_transcript(conn, video_id, video_title, video_transcript):
    cursor = conn.cursor()

    print("Trying to insert single transcript: ")
    print(f"video_id:{video_id}")
    print(f"video_title: {video_title}")
    print(f"video_transcript: {video_transcript[:10]}")
 
    sql_statement = '''
        INSERT INTO transcripts (video_id, video_title, video_transcript)
        VALUES (?, ?, ?)
    '''

    cursor.execute(sql_statement, (
        video_id, video_title, video_transcript
    ))

    conn.commit()
    print(f"Successfully inserted whole transcript of video_ID: {video_id}")


#-----------------------------------------------------------------------------------#

# Save all data related to a video: metadata, timestamps, transcript chunks
def insert_video_data(conn, video_data):
    try: 
        cursor = conn.cursor()
        
        # Insert video metadata into the videos table
        sql_statement = '''
            INSERT INTO videos (video_id, title, channel, description)
            VALUES (?, ?, ?, ?)
        '''
        cursor.execute(sql_statement, (
            video_data["video_id"],
            video_data["title"],
            video_data["channel_name"],
            video_data["description"]
        ))

        conn.commit()
        print(f"Successfully inserted video metadata for video_id: {video_data['video_id']}")

        if (video_data["has_timestamps"]):
            # Now insert the timestamps into the timestamps table
            print(" - video has timestamps - try")
            insert_transcript_chunks(conn, video_data["video_id"], video_data["grouped_transcripts"])
            print(f"Successfully inserted timestamps data for video_id: {video_data['video_id']}")
        
        # Regardless of transcript presence, insert the entire transcript too
        insert_single_transcript(conn, video_data["video_id"], video_data["title"], video_data["single_transcript"])
        print(f"Successfully inserted single_transcript for video_id: {video_data['video_id']}")

        # Now insert the transcript chunks
        # insert_transcript_chunks(conn, video_data["video_id"], video_data["grouped_transcripts_array"])
        print(f"Finished insertion for video_id: {video_data['video_id']}")

    except sqlite3.Error as e:
        print(f"Error inserting video data into database: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while inserting data into the database: {e}")


# Function to retrieve a single_transcript for a specific episode
def get_single_transcript(conn, youtube_video_id):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT video_transcript
        FROM transcripts
        WHERE video_id = ?          
    ''', (youtube_video_id,))
    
    return cursor.fetchall()

def get_chunked_transcripts(conn, youtube_video_id):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT transcript_Chunk
        FROM timestamps
        WHERE video_id = ?          
    ''', (youtube_video_id,))
    
    return cursor.fetchall()


