from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

DEVELOPER_KEY = 'AIzaSyAM-HaQhckbu48StmuiUtFXFrGUasET_y4'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)


search_response = youtube.search().list(
    q = '로파이',
    order = 'date',
    part = 'snippet',
    maxResults = 1
).execute()



videoId = []
for i in search_response['items']:
    if i['id']['kind']=='youtube#video':
        videoId.append((i['id']['videoId'], i['snippet']['title']))
        print(i)


print(videoId)


