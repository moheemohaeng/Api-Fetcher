from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser


DEVELOPER_KEY = 'your developer key'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)


# cost : 1

def channel_list(channel_id):
    channel_response = youtube.channels().list(
        id = channel_id,
        part = 'contentDetails', # id, snippet, ...
        maxResults = 10 # 0 ~ 50
    ).execute()
    
    return channel_response # return json