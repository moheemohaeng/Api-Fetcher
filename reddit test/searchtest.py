from hashlib import new
from pymongo import MongoClient
import os
import asyncio
import logging
import sys
import praw
import json
from bson import json_util
from datetime import datetime
import shutil
from pathlib import Path



CLIENT_ID = 'aD4mb7E2SBstq9l8HgvfLg'
CLIENT_SECRET = 'lKqkCVN3NtSyyyBK3YZQHpLKoBP-wQ'
USER_AGENT = 'moheetest'
SUB_REDDIT = 'game'
LIMIT = 80


reddit = praw.Reddit(client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    user_agent = USER_AGENT)

# os.mkdir('//wsl$/Ubuntu-20.04/home/kdh0216/meta')
# os.mkdir('//wsl$/Ubuntu-20.04/home/kdh0216/data')
# for real_subreddit in reddit.subreddits.search(SUB_REDDIT) :
#     print(real_subreddit.display_name)
#     print()
#     for real_submission in reddit.subreddit(real_subreddit.display_name).hot(limit = 1):
#         print(real_submission.title)
#     print()

for real_submission in reddit.subreddit('all').search('game', sort = new):
    print(real_submission.title)
print()

