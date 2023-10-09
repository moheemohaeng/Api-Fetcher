from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser


DEVELOPER_KEY = 'your developer key'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)


# cost : 1

def commentThreads_list(video_Id):
    commentThreads_response = youtube.commentThreads().list(
        videoId = video_Id,
        textFormat = 'plainText',
        part = 'id, snippet', # id, snippet, replies
        maxResults = 50 # 0 ~ 50
    ).execute()

    return commentThreads_response # return json