from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser


DEVELOPER_KEY = 'your developer key'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)


# cost : 100

def search_list(search_keyword):
    search_response = youtube.search().list(
        q = search_keyword,
        order = 'relevance', # rating, relevance, title, videoCount, ViewCount...
        part = 'snippet', # id, snippet
        maxResults = 50 # 0 ~ 50
    ).execute()

    return search_response # return json