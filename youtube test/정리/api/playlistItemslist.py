from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser


DEVELOPER_KEY = 'your developer key'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)


# cost : 1

def playlistItems_list(playlist_Id):
    playlistItems_response = youtube.playlistItems().list(
        playlistId = playlist_Id,
        part = 'snippet', # id, snippet, ...
        maxResults = 50 # 0 ~ 50
    ).execute()

    return playlistItems_response # return json