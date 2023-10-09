import praw
import csv
import time
from datetime import datetime
import json
from pymongo import MongoClient
from bson import json_util
import os
from nwlib.protocol.fetched_result import FetchedResult
from pathlib import Path
from pymongo import MongoClient

CLIENT_ID = 'aD4mb7E2SBstq9l8HgvfLg'
CLIENT_SECRET = 'lKqkCVN3NtSyyyBK3YZQHpLKoBP-wQ'
USER_AGENT = 'moheetest'


SUB_REDDIT = 'game'
LIMIT = 999

host = 'localhost'
port = '27017'
mongo = MongoClient(host, int(port))

result_fetch = FetchedResult()

reddit = praw.Reddit(client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    user_agent = USER_AGENT)

def commentslist_(commentforest, meta_path):
    global mongo


    commentforest.replace_more(limit = 10)
    for comment in commentforest.list():
        file_path = 'C:/Users/user/Desktop/reddit test/data/'+comment.id+'.json'
        if comment.reply is not None:
            commentslist_(comment.replies, meta_path)
        try:
            _comment = {'id':comment.id, 'link_id':comment.link_id, 'parent_id':comment.parent_id, 'body':comment.body,
                'author':{'id':comment.author.id, 'name':comment.author.name, 'created_utc(unix)':comment.author.created_utc},
                'score':comment.score, 'created_utc(unix)':comment.created_utc, 'permalink':comment.permalink, 'edited':comment.edited,
                }

        except:
            _comment = {'id':comment.id, 'link_id':comment.link_id, 'parent_id':comment.parent_id, 'body':comment.body,
                'author':'deleted',
                'score':comment.score, 'created_utc(unix)':comment.created_utc, 'permalink':comment.permalink,
                }



        with open(file_path, 'w', encoding='UTF-8') as file:
            json.dump(_comment, file, default=json_util.default, indent = 10, ensure_ascii=False)
        
        mongo["reddit"]["comment"].insert_one(_comment).inserted_id
        
        result_fetch.add_file(file_name = comment.id, meta_file_path = Path(meta_path), data_file_path = Path(file_path))





while(True):


    os.mkdir('C:/Users/user/Desktop/reddit test/meta')
    os.mkdir('C:/Users/user/Desktop/reddit test/data')
    for real_subreddit in reddit.subreddits.search('marvel') :


        for real_submission in reddit.subreddit(real_subreddit.display_name).hot(limit = 80):
            meta_path = 'C:/Users/user/Desktop/reddit test/meta/'+real_subreddit.display_name+'_'+real_submission.name+'_meta.json'
            
            try:
                meta = {'python_version':'Python 3.10.2', 'praw_version':'7.5.0', 'client_id': CLIENT_ID, 'client_secret':CLIENT_SECRET, 'user_agent': USER_AGENT,
                    'subreddit':{'id':reddit.subreddit(real_subreddit.display_name).id, 'display_name':real_subreddit.display_name, 'name':real_subreddit.name, 
                        'description':real_subreddit.description, 'created_utc(unix)':real_subreddit.created_utc},
                    'submission':{'id':real_submission.id, 'name':real_submission.name, 'title':real_submission.title, 
                        'author':{'id':real_submission.author.id,'name':real_submission.author.name, 'created_utc(unix)':real_submission.author.created_utc},
                        'self_text':real_submission.selftext, 'score':real_submission.score,'created_utc(unix)':real_submission.created_utc, 'permalink':real_submission.permalink, 'url':real_submission.url}}
            except:
                meta = {'python_version':'Python 3.10.2', 'praw_version':'7.5.0', 'client_id': CLIENT_ID, 'client_secret':CLIENT_SECRET, 'user_agent': USER_AGENT,
                    'subreddit':{'id':real_subreddit.id, 'display_name':real_subreddit.display_name, 'name':real_subreddit.name, 
                        'description':real_subreddit.description, 'created_utc(unix)':real_subreddit.created_utc},
                    'submission':{'id':real_submission.id, 'name':real_submission.name, 'title':real_submission.title, 
                        'author':'deleted',
                        'self_text':real_submission.selftext, 'score':real_submission.score,'created_utc(unix)':real_submission.created_utc, 'permalink':real_submission.permalink, 'url':real_submission.url}}


            with open(meta_path, 'w', encoding='UTF-8') as file:
                json.dump(meta, file, default=json_util.default, indent = 10, ensure_ascii=False)
            mongo["reddit"]["meta"].insert_one(meta).inserted_id

            commentslist_(real_submission.comments, meta_path)
            
            # comments_list = {'comments':[]}
            # for comment in real_submission.comments.list():
            #     try:
            #         _comment = {'id':comment.id, 'body':comment.body,
            #             'author':{'id':comment.author.id, 'name':comment.author.name, 'created_utc(unix)':comment.author.created_utc},
            #             'score':comment.score, 'created_utc(unix)':comment.created_utc, 'permalink':comment.permalink}
            #     except:
            #         _comment = {'id':comment.id, 'body':comment.body,
            #             'author':'deleted',
            #             'score':comment.score, 'created_utc(unix)':comment.created_utc, 'permalink':comment.permalink}
            #     comments_list['comments'].append(_comment)


            

    
            # host = '192.168.1.45'
            # port = '25017'
            # mongo = MongoClient(host, int(port))
            # mongo["text"]["text"].insert_one(meta).inserted_id
            # mongo["text"]["text"].insert_one(comments_list).inserted_id
            






# for subreddit in reddit.subreddits.search('game', limit = 10):
#     print(subreddit.id, subreddit.display_name)

# for submission in reddit.subreddit('game').search('game'):
#     print(submission.id, submission.url)