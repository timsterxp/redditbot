#!/usr/bin/python3.7
#Removed MySQL info/Subreddit Details for Github Usage/File Example

import praw
import pdb
import re
import os
import datetime
import time
import mysql.connector



reddit = praw.Reddit('BOTNAME/CONFIG')
subreddit=reddit.subreddit('SUBREDDITNAME')
#fileName = fileName

conversations = reddit.subreddit(subreddit).modmail.conversations(state="mod")
for message in conversation.messages:
    print(message.body_markdown)
    
    