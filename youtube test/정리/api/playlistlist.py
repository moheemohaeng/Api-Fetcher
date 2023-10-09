from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser


DEVELOPER_KEY = 'your developer key'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)


# cost : 1

def playlist_list(channel_Id):
    playlist_response = youtube.playlist().list()(
        channelId = channel_Id,
        part = 'id, snippet', # id, snippet, status
        maxResults = 50 # 0~ 50
    ).execute()

    return playlist_response # return json