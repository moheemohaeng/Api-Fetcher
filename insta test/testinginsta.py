from instagrapi import Client
import schedule
import time
import json
from pymongo import MongoClient
from pathlib import Path
from requests import Session
from bson import json_util
import os


host = '192.168.1.45'
port = '25017'
# host = 'local'
# port = '27017'
mongo = MongoClient(host, int(port))

proxy_host = "proxy.crawlera.com"
proxy_port = "8011"
proxy_auth = "7ccd51590e6c4f7c9841b646598dcc52:"
proxy_addr = f"http://{proxy_auth}@{proxy_host}:{proxy_port}/"
crt_path = Path("zyte-smartproxy-ca.crt")

# cl = Client(proxy="socks5h://127.0.0.1:9150")
cl = Client()
# cl.public.verify = cl.private.verify = str(crt_path.absolute())
# cl = Client()
cl.login('zofldjemforhs', 'her6792ya!')

user_list = ['duckjungkimduckcentregim', 'watermin_jung', '99_99duck', 'jiji.0.ijij', 'eix__cosx_isinx', '13e_positive',
    'okj_rlj', 'suu_out', 'soooojiinn', 'ds.wook', 'chae_cho', 'moassaang', 'im_winwater', 'da_lotus__', 'gini_._._', 'jo_o_han',
    'yeongeunkim_', 'kkkkkkk__yu', 'hanbyeol_813', 'tthwaa', 'dearhee__', 'mxrninx', 'ss.miiin_', 'ryong_rr', 'hanbyol_sun', 
    'moong__zzi', 'jooseok.0527', 'aestas_na', 'narngreen' , 'kozzy_h', 'strongzero_kr', 'happihee']

tag_list = ['조던', '성수카페', '군인', '병장', '의경', '의경스타그램', '고등학생', '기타', '유희열', '아이유',
    '가요', '가요대축제', '가요대전', '방탄소년단', '방탄', '방탄진', '방탄지민', '대학로맛집', '대학', '대학로카페', '대학생', '대학로핫플',
    '대학생코디', '대학로데이트', '데스노트', '뮤지컬', '여행', '여행사진', '여행스타그램', '여행에미치다', '여행중', '출근', '퇴근', '강남',
    '건대', '건대맛집', '왕십리맛집', '강남맛집', '셀피', '홍대', '홍대사진', '홍대공연', '길거리공연', '코딩', '학원', '퇴사', '칼퇴', '제주도',
    '비행기', '거북이', '강아지', '고양이', '강하늘', '강아지일상', '드라마', '영화', '마블']

# for id in user_list:

# print('collecting : ','watermin_jung', '=============================================')
# try:
    # user_id = cl.user_id_from_username('mohee_mohaeng')
    # medias = cl.user_medias(user_id, 1)
    # print(medias)
    # search = cl.search_hashtags('game')
    # print(search)
# except:
#     print('user not found--------------------------------')

#해시태그로 글검색하기 (최근, 인기기준)
# result = cl.hashtag_medias_recent('낙산공원', amount = 1)
# result = cl.hashtag_medias_top('낙산공원', amount = 1)

# print(result[0].id)

#미디어 아이디로 댓글들 조회
# comments = cl.media_comments(media_id= result[0].id, amount = 1)
# print(comments[0].dict())
# print()


def media_in_medias(medias):
    for media in medias:
        meta_path = 'C:/Users/user/Desktop/insta test/meta/'+media.id+'_meta.json'
        print('<<< collecting media: ', media.title, ' >>>')
        try:
            meta = cl.media_info(media.id).dict()
        except:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!fail read media : ', media.title, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('-----------', media.title, ' : meta data on------------')

        with open(meta_path, 'w', encoding='UTF-8') as file:
            json.dump(meta, file, default=json_util.default, indent=8, ensure_ascii=False)
        mongo["insta_test"]["meta"].insert_one(meta).inserted_id

        comments = cl.media_comments(media_id=media.id, amount = 500)
        comment_in_comments(comments, meta_path)



def comment_in_comments(comments, meta_path):
    for comment in comments:
        file_path = 'C:/Users/user/Desktop/insta test/data/'+comment.pk+'.json'
        try:
            comment_info = comment.dict()
        except:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!fail read comment : ', comment.pk, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

        print('-----------', comment.pk, ' : comment data on------------')

        with open(file_path, 'w', encoding='UTF-8') as file:
            json.dump(comment_info, file, default=json_util.default, indent=8, ensure_ascii=False)
        
        mongo["insta_test"]["comment"].insert_one(comment_info).inserted_id
    




def main_run():
    for tag in tag_list:
        print("================================= Tag : ", tag, '=================================')

        try:
            medias = cl.hashtag_medias_top(tag, amount = 20)
            media_in_medias(medias)
            
        except:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!fail read tag : ', tag, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')










if __name__ =='__main__':
    os.mkdir('C:/Users/user/Desktop/insta test/meta')
    os.mkdir('C:/Users/user/Desktop/insta test/data')
    main_run()
    schedule.every(1).minutes.do(main_run)
    while True:
        schedule.run_pending()
        time.sleep(1)


