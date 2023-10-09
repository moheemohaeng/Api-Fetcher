from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser


DEVELOPER_KEY = 'your developer key'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)



usage_point = 0


def get_comment_threads(youtube, video_id, comment_num):
    results = youtube.commentThreads().list(
        part = 'snippet',
        videoId = video_id,
        textFormat = 'plainText',
        maxResults = comment_num
    ).execute()

    comment_list = []
    for item in results['items']:
        comment_id = item['id']
        comment = item['snippet']['topLevelComment'] 
        author = comment['snippet']['authorDisplayName']
        publishedAt = comment['snippet']['publishedAt'] 
        text = comment['snippet']['textDisplay'] 
        comment_list.append((comment_id, author, publishedAt, text))

    for (comment_id, author, publishedAt, text) in comment_list:
        print(f'[ Comment ID: {comment_id} / author: {author} / date: {publishedAt} ]')
        print(f'[text: {text}]')




def know_channel_id(video_id):
    request = youtube.videos().list(
        part = 'snippet',
        id = video_id
    )
    response = request.execute()
    channel_id = response['items'][0]['snippet']['channelId']

    return channel_id




def channels_threads(youtube, channel_id):
    channels_response = youtube.channels().list(
        id = channel_id,
        part = 'contentDetails',
        maxResults = 10
    ).execute()
    channel = channels_response['items'][0]
    uploads_playlist_id = channel['contentDetails']['relatedPlaylists']['uploads']

    
    playlistitems_list_request = youtube.playlistItems().list(
        playlistId = uploads_playlist_id,
        part = 'snippet',
        maxResults = 50
    )
    cnt = 0
    last = 10 
    video_list = []
    
    
    while playlistitems_list_request:
        playlistitems_list_response = playlistitems_list_request.execute()
        
        for playlist_item in playlistitems_list_request['items']:
            video_id = playlist_item['snippet']['resourceId']['videoId']
            title = playlist_item['snippet']['title']
            video_list.append((video_id, title))
            cnt += 1
            if cnt >= last:
                break
        
        if cnt >= last:
            break
        playlistitems_list_request = youtube.playlistItems().list_next(playlistitems_list_request, playlistitems_list_response)

    return video_list






def keyword_search(keyword):
    search_response = youtube.search().list(
        q = keyword,
        order = 'relevance', #rating, relevance, title, videoCount, ViewCount
        part = 'snippet',
        maxResults = 30
    ).execute()

    video_list = []
    for i in search_response['items']:
        if i['id']['kind']=='youtube#video':
            video_list.append((i['id']['videoId'], i['snippet']['title']))


    return video_list






def _main():
    video_list = keyword_search('s2w lab')
    for (video_id, title) in video_list:
        print(f'<<Video ID: {video_id} / Title: {title}>>')
        try:
            get_comment_threads(youtube, video_id, 1)
        except: #live video
            print("no comment.")


if __name__ == "__main__":
    _main()