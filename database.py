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
        """CREATE TABLE IF NOT EXISTS transcripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            youtube_video_id TEXT,
            title TEXT,
            description TEXT,
            channel_name TEXT,
            transcript TEXT
        );""",

        """CREATE TABLE IF NOT EXISTS timestamps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            episode_id INTEGER,
            timestamp INTEGER,
            text TEXT,
            FOREIGN KEY (episode_id) REFERENCES episodes(id)
        );"""]

    # create a database connection
    try:
        cursor = conn.cursor()
        for statement in sql_statements:
            cursor.execute(statement)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

# Function to insert a video and its corresponding transcript
# The transcript is first stored as a single text file
def insert_transcript(conn, video_id, video_data):
    cursor = conn.cursor()
    sql_statement = '''
        INSERT INTO transcripts (youtube_video_id, title, description, channel_name, transcript) VALUES (?, ?, ?, ?, ?)
    '''
    try: 
        
        cursor.execute('''
                INSERT INTO transcripts (youtube_video_id, title, description, channel_name, transcript) VALUES (?, ?, ?, ?, ?)
        ''', (
            video_id,
            video_data["title"],
            "description",
            video_data["channel_name"],
            "transcript"
        ))

        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError as e:
        print(f"Integrity Error (likely a duplicate youtube_video_id): {e}")
    except sqlite3.Error as e:
        print(f"SQL Error: {e}")
    except KeyError as e:
        print(f"KeyError: Missing field in video_data: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

# Function to insert timestamps and their labels for a specific video
# the input 'timestamps' is an array of dicts
def insert_timestamps(conn, episode_id, timestamps):
    cursor = conn.cursor()
    
    for entry in timestamps:
        cursor.execute('''
            INSERT INTO timestamps (episode_id, timestamp, text)
            VALUES (?, ?, ?)
        ''', (episode_id, entry["timestamp"], entry["text"]))
    
    conn.commit()

#-----------------------------------------------------------------------------------#

# Function to retrieve transcripts for a specific episode
def get_transcripts(conn, youtube_video_id):
    cursor = conn.cursor()

    cursor.execute('''
        SELECT transcripts.text
        FROM transcripts
        JOIN episodes ON transcripts.episode_id = episodes.id
        WHERE episodes.youtube_video_id = ?
    ''', (youtube_video_id,))
    
    return cursor.fetchall()

