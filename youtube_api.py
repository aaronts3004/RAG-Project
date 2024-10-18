
''' Central API initialization script'''
import os
from dotenv import load_dotenv

# API modules
# Google
from googleapiclient.discovery import build
import googleapiclient.errors
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

load_dotenv()
DEVELOPER_KEY_1 = os.getenv("GOOGLE_API_KEY")

api_service_name = "youtube"
api_version = "v3"

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Youtube
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY_1)

# Function to initialize and return the YouTube API client
def get_youtube_client():
    return build(api_service_name, api_version, developerKey=DEVELOPER_KEY_1)