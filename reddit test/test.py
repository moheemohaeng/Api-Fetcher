import praw
import csv
import time
from datetime import datetime

CLIENT_ID = 'aD4mb7E2SBstq9l8HgvfLg'
CLIENT_SECRET = 'lKqkCVN3NtSyyyBK3YZQHpLKoBP-wQ'
USER_AGENT = 'moheetest'
SUB_REDDIT = 'korea'
LIMIT = 999

def scrap_reddit():
    reddit = praw.Reddit(client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    user_agent = USER_AGENT)

    print('============')
    print("Scrapping Reddit Submission")
    print("=============")

    scrap_data = []
    total_subreddit = 0

    for submission in reddit.subreddit(SUB_REDDIT).hot(limit=LIMIT):
        total_subreddit += 1
        submission_dict = vars(submission)

        #TITLE
        print('[Title %03d] : ' % (total_subreddit), submission.title)
        writelist = [datetime.utcfromtimestamp(submission.created_utc),
        submission.title,
        submission_dict['selftext'].rstrip('\n'), 0]

        #COMMENT
        post = reddit.submission(id = submission_dict['id'])
        total_cmt = 0
        for top_level_comment in post.comments:
            writelist.append(top_level_comment.body.rstrip('\n'))
            total_cmt += 1


        writelist[3] = total_cmt
        scrap_data.append(writelist)
        print(writelist)
        print('---------------------------')
    
    return scrap_data, total_subreddit



scrap_data, total_subreddit = scrap_reddit()
print(scrap_data)