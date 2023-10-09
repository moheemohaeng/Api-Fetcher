import praw
import csv
import time
from datetime import datetime
import json

CLIENT_ID = 'aD4mb7E2SBstq9l8HgvfLg'
CLIENT_SECRET = 'lKqkCVN3NtSyyyBK3YZQHpLKoBP-wQ'
USER_AGENT = 'moheetest'
SUB_REDDIT = 'game'
LIMIT = 999

def moreCom(com, count) :
    count2 = count
    comment = com.comments
    print("")
    print("")
    print("")
    print(comment)
    print("asdfasdf")
    print("")
    print("")
    print("")

    for comment in com.comments:
        if hasattr(comment, 'body') != True:
            return moreCom(comment, count)
        else:
            count2 += 1
            print("====", count2, " comment : ", comment.body.rstrip('\n'), " ==== ")


reddit = praw.Reddit(client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    user_agent = USER_AGENT)

while(True):
    counting = 1
    for real_subreddit in reddit.subreddits.search('korea') :
        print("<<<<<<<<<<< ", counting, " subreddit : ",real_subreddit.display_name,">>>>>>>>>>>>>>>>>>>>>>")
        print("")
        counting2 = 1
        for real_submission in reddit.subreddit(real_subreddit.display_name).hot(limit = 80) :
            print("-------------", counting2, " submission : ", real_submission.title,'---------------------')
            count = 0
            for comment in real_submission.comments : 
                count += 1
                if hasattr(comment, 'body') != True:
                    moreCom(comment, count)
                else:
                    print("====", count, " comment : ", comment.body.rstrip('\n'), " ==== ")
                
                # if count == 101 :
                #      break
            print("")
            counting2 += 1
        print("")
        print("")
        print("==============================================================")
        counting += 1

        
# for subreddit in reddit.subreddits.search('game', limit = 10):
#     print(subreddit.id, subreddit.display_name)

# for submission in reddit.subreddit('game').search('game'):
#     print(submission.id, submission.url)