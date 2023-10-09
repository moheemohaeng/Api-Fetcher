from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser


DEVELOPER_KEY = 'AIzaSyAM-HaQhckbu48StmuiUtFXFrGUasET_y4'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)






#영상 댓글 불러오기
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
        comment = item['snippet']['topLevelComment'] #댓글정보
        author = comment['snippet']['authorDisplayName'] #댓글작정자
        publishedAt = comment['snippet']['publishedAt'] #댓글 작성 날짜
        text = comment['snippet']['textDisplay'] #댓글내용
        comment_list.append((comment_id, author, publishedAt, text))

    for (comment_id, author, publishedAt, text) in comment_list:
        print(f'[ Comment ID: {comment_id} / 작성자: {author} / 작성 날짜: {publishedAt} ]')
        print(f'[내용: {text}]')




#비디오 id받아서 채널 id따오기
def know_channel_id(video_id):
    request = youtube.videos().list(
        part = 'snippet',
        id = video_id
    )
    response = request.execute()
    channel_id = response['items'][0]['snippet']['channelId']

    return channel_id






#채널 영상리스트, 정보 가져오기
def channels_threads(youtube, channel_id):
    channels_response = youtube.channels().list(
        id = channel_id,
        part = 'contentDetails',
        maxResults = 10
    ).execute()
    channel = channels_response['items'][0]
    uploads_playlist_id = channel['contentDetails']['relatedPlaylists']['uploads']

    #각 영상들 정보 가져오기
    playlistitems_list_request = youtube.playlistItems().list(
        playlistId = uploads_playlist_id,
        part = 'snippet',
        maxResults = 50
    )
    cnt = 0
    last = 10 #갯수제한
    video_list = []
    
    #각 영상들 id, title 따로 저장. 필요시 변수추가로, 썸네일도 가능
    while playlistitems_list_request:
        playlistitems_list_request = playlistitems_list_request.execute()
        #각 영상에 대한 정보
        for playlist_item in playlistitems_list_request['items']:
            video_id = playlist_item['snippet']['resourceId']['videoId'] #영상 id
            title = playlist_item['snippet']['title'] #영상 제목
            video_list.append((video_id, title))
            cnt += 1
            if cnt >= last:
                break
        
        if cnt >= last:
            break
        playlistitems_list_request = youtube.playlistItems().list_next(playlistitems_list_request, playlistitems_list_response)

    return video_list







#키워드 검색 결과 비디오 id 뽑아오기
def keyword_search(keyword):
    search_response = youtube.search().list(
        q = keyword,
        order = 'relevance', #정렬 날짜순, rating, relevance, title, videoCount, ViewCount
        part = 'snippet',
        maxResults = 30
    ).execute()

    video_list = []
    for i in search_response['items']:
        if i['id']['kind']=='youtube#video': #재생목록이나 채널결과는 제외. 추가 가능.
            video_list.append((i['id']['videoId'], i['snippet']['title']))


    return video_list







video_list = keyword_search('kpop')
for (video_id, title) in video_list:
    print(f'<<Video ID: {video_id} / 제목: {title}>>')
    try:
        get_comment_threads(youtube, video_id, 1)
    except: #라이브의 경우 잡히지 않음.
        print("댓글이 없습니다.")