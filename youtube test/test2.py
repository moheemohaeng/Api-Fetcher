import pandas

from googleapiclient.discovery import build

api_key = 'AIzaSyAM-HaQhckbu48StmuiUtFXFrGUasET_y4'
video_id = 'Zrh_v5kLdV0'
youtube = build('youtube', 'v3', developerKey=api_key)
#비디오 id받아서 채널 id따오기
def know_channel_id(video_id):
    request = youtube.videos().list(
        part = 'snippet',
        id = video_id
    )
    response = request.execute()
    channel_id = response['items'][0]['snippet']['channelId']

    return channel_id

print(know_channel_id(video_id))