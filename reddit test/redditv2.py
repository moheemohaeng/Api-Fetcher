import praw

from datetime import datetime
import json
from pymongo import MongoClient
from bson import json_util
import os
from nwlib.protocol.fetched_result import FetchedResult
from pathlib import Path
from pymongo import MongoClient
import time
from requests import Session
import requests
import schedule
import shutil


CLIENT_ID = 'aD4mb7E2SBstq9l8HgvfLg'
CLIENT_SECRET = 'lKqkCVN3NtSyyyBK3YZQHpLKoBP-wQ'
USER_AGENT = 'moheetest'


# SUB_REDDIT_LIST = ['formula1', 'nba', 'Boxing', 'baseball', 'LiverpoolFc', 'tennis', 'reddevils', '49ers', 'suns', 'warriors',
#                     'wow', 'NintendoSwitch', 'leagueoflegends', 'xboxone', 'thesims', 'skyrim', 'GlobalOffensive', 'pokemongo', 'Eve', 'DestinyTheGame',
#                     'UpliftingNews', 'savedyouaclick', 'olympics', 'gamernews', 'nottheonion', 'offbeat', 'technews', 'news', 'worldnews',
#                     'marvelstudios', 'OnePiece', 'Spiderman', 'batman', 'netflix', 'rickandmorty', 'IASIP', 'BlackClover', 'community', 'gameofthrones',
#                     'travel', 'europe', 'australia', 'LegalAdviceUK', 'mexico', 'ScottishPeopleTwitter', 'EarthPorn', 'ich_iel', 'newzealand', 'berkeley',
#                     'technology', 'gadgets', 'apple', 'GooglePixel', 'softwaregore', 'cscareerquestions', 'computers', 'Android', 'Machinists', 'cordcutters',
#                     'kpop', 'audiophile', 'deathgrips', 'headphones', 'popheads', 'vinyl', 'indieheads', 'ifyoulikeblank', 'Guitar', 'listentothis',
#                     'MakeupAddiction', 'femalefashionadvice', 'malelivingspace', 'OUTFITS', 'yeezys', 'beauty', 'findfashion', 'malehairadvice', 'fragrance', 'beards',
#                     'PersonalFinanceCanada', 'StockMarket', 'jobs', 'Target', 'realestateinvesting', 'WorkOnline', 'startups', 'beermoney', 'Entrepreneur', 'StudentLoans',
#                     'science', 'YouShouldKnow', 'Documentaries', 'dataisbeautiful', 'whatisthisthing', 'OutOfTheLoop', 'askscience', 'todayilearned', 'Awwducational', 'savedyouaclick']
SUB_REDDIT_LIST = ['AccessCyber', 'apple', 'AskNetsec', 'BadApps', 'blackhat', 'blueteamsec', 'cissp', 'CompTIA', 'computerforensics',
                'ComputerSecurity', 'crypto', 'cyber', 'cyberlaws', 'cybersecurity', 'Cybersecurity101', 'CyberSecurityJobs', 'datarecovery',
                'ethicalhacking', 'ExploitDev', 'fulldisclosure', 'HackBloc', 'hackers', 'hackersec', 'hacking', 'Hacking_Tutorials', 'HowToHack',
                'i2p', 'Information_Security', 'InfoSecNews%20-', 'IoTSecurity101', 'MacOs', 'macsysadmin', 'Malware', 'msp', 'netsec',
                'netsecstudents', 'NetworkSecurity', 'opendirectories', 'osx', 'privacy', 'pwned', 'redteamsec', 'regames', 'reverseengineering', 'SecurityCareerAdvice',
                'securityCTF', 'TOR', 'websecurity', 'zeroday', 'antivirus', 'LinuxMalware']

host = '192.168.1.45'
port = '25017'
mongo = MongoClient(host, int(port))

result_fetch = FetchedResult()

proxy_host = "proxy.crawlera.com"
proxy_port = "8011"
proxy_auth = "7ccd51590e6c4f7c9841b646598dcc52:"
crt_path = Path("zyte-smartproxy-ca.crt")
session = Session()
session.proxies['https'] = f"http://{proxy_auth}@{proxy_host}:{proxy_port}/"
session.verify = str(crt_path)

reddit = praw.Reddit(client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    user_agent = USER_AGENT,
    requestor_kwargs={'session': session})

def read_commentforest(commentforest, meta_path):

    commentforest.replace_more(limit = 10)

    for comment in commentforest.list():
        file_path = 'C:/Users/user/Desktop/reddit test/data/'+comment.id+'.json'
        # if comment.reply is not None:
        #     read_commentforest(comment.replies, meta_path)
        try:
            comment_info = {'id':comment.id, 
            'parent_id':comment.parent_id, 
            'body':comment.body,
            'author_id':comment.author.id,
            'author_name':comment.author.name,
            'author_created_utc(unix)':comment.author.created_utc,
            'score':comment.score, 
            'created_utc(unix)':comment.created_utc, 
            'permalink':comment.permalink,
                }

        except:
            comment_info = {'id':comment.id, 
            'parent_id':comment.parent_id, 
            'body':comment.body,
            'author':'deleted',
            'author_name':'deleted',
            'author_created_utc(unix)':'deleted',
            'score':comment.score, 
            'created_utc(unix)':comment.created_utc, 
            'permalink':comment.permalink,
                }

        print('-----------', comment.id,' : comment data on------------')        


        with open(file_path, 'w', encoding='UTF-8') as file:
            json.dump(comment_info, file, default=json_util.default, indent = 10, ensure_ascii=False)
        
        mongo["reddit_ti"]["comment"].insert_one(comment_info).inserted_id
        
        result_fetch.add_file(file_name = comment.id, meta_file_path = Path(meta_path), data_file_path = Path(file_path))



def submission_in_subreddit(subreddit_name):
    for submission in reddit.subreddit(subreddit_name).new():
        meta_path = 'C:/Users/user/Desktop/reddit test/meta/'+subreddit_name+'_'+submission.name+'_meta.json'
        print('<<< collecting submission: ', submission.name, ' >>>')
        try:
            meta = {'python_version':'Python 3.10.2', 'praw_version':'7.5.0', 'client_id': CLIENT_ID, 'client_secret':CLIENT_SECRET, 'user_agent': USER_AGENT,
            'subreddit_id':reddit.subreddit(subreddit_name).id,
            'subreddit_display_name':reddit.subreddit(subreddit_name).display_name,
            'subreddit_name':reddit.subreddit(subreddit_name).name,
            'subreddit_description':reddit.subreddit(subreddit_name).description,
            'subreddit_created_utc(unix)':reddit.subreddit(subreddit_name).created_utc,
            'submission_id':submission.id,
            'submission_name':submission.name,
            'submission_title':submission.title,
            'submission_author_id':submission.author.id,
            'submission_author_name':submission.author.name,
            'submission_author_created_utc(unix)':submission.author.created_utc,
            'submission_self_text':submission.selftext, 'submission_score':submission.score,'submission_created_utc(unix)':submission.created_utc, 
            'submission_permalink':submission.permalink, 'submission_url':submission.url}
        except:
            meta = {'python_version':'Python 3.10.2', 'praw_version':'7.5.0', 'client_id': CLIENT_ID, 'client_secret':CLIENT_SECRET, 'user_agent': USER_AGENT,
            'subreddit_id':reddit.subreddit(subreddit_name).id,
            'subreddit_display_name':reddit.subreddit(subreddit_name).display_name,
            'subreddit_name':reddit.subreddit(subreddit_name).name,
            'subreddit_description':reddit.subreddit(subreddit_name).description,
            'subreddit_created_utc(unix)':reddit.subreddit(subreddit_name).created_utc,
            'submission_id':submission.id,
            'submission_name':submission.name,
            'submission_title':submission.title,
            'submission_author_id':'deleted',
            'submission_author_name':'deleted',
            'submission_author_created_utc(unix)':'deleted',
            'submission_self_text':submission.selftext, 'submission_score':submission.score,'submission_created_utc(unix)':submission.created_utc, 
            'submission_permalink':submission.permalink, 'submission_url':submission.url}

        print('-----------', submission.name, ' : meta data on------------')
        print('-----------', submission.num_comments, ' : comments------------')

        
        with open(meta_path, 'w', encoding='UTF-8') as file:
            json.dump(meta, file, default=json_util.default, indent = 10, ensure_ascii=False)
        mongo["reddit_ti"]["meta"].insert_one(meta).inserted_id

        read_commentforest(submission.comments, meta_path)










def main_run():

    for subreddit_name in SUB_REDDIT_LIST:
        print("================================= SUBREDDIT : ", subreddit_name, '=================================')
        try:
            submission_in_subreddit(subreddit_name)
        except:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!fail read subreddit : ', subreddit_name, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    # if os.path.exists('C:/Users/user/Desktop/reddit test/meta') :
        #     shutil.rmtree('C:/Users/user/Desktop/reddit test/meta')
    # if os.path.exists('C:/Users/user/Desktop/reddit test/data') :    
        #     shutil.rmtree('C:/Users/user/Desktop/reddit test/data')


if __name__ =='__main__':
    # os.mkdir('C:/Users/user/Desktop/reddit test/meta')
    # os.mkdir('C:/Users/user/Desktop/reddit test/data')
    main_run()
    schedule.every(45).minutes.do(main_run)
    while True:
        schedule.run_pending()
        time.sleep(1)
