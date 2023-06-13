#!/usr/bin/python3.7
#Removed MySQL info/Subreddit Details for Github Usage/File Example

import praw
import pdb
import re
import os
import datetime
import time




reddit = praw.Reddit('BOTNAME/CONFIG')
subreddit=reddit.subreddit('SUBREDDITNAME')
fileName = "mail_replied_to.txt"

if not os.path.isfile(fileName):
    mail_replied_to = []

# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open(fileName, "r") as f:
        mail_replied_to = f.read()
        mail_replied_to = mail_replied_to.split("\n")
        mail_replied_to = list(filter(None, mail_replied_to))
        
conversations = subreddit.modmail.conversations(state="mod")
        
for eachConvo in conversations:
    if (eachConvo.num_messages>1):
        print ("There is more than 1 message! We found: ")
        print(eachConvo.num_messages)
        #A secondary check to ensure we arent spamming users
        continue
    if (eachConvo.id not in mail_replied_to):
        print ("Yes this was not found previously!")
        #Add it to the list before doing any actions 
        mail_replied_to.append(eachConvo.id)
        message = "Super long reply message testing"
        eachConvo.reply(body=message)
        eachConvo.archive()
        
        
        
        
           
    