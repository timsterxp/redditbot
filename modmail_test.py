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
        
#State can be new/all/archived/etc
        
state = "mod"
        
        
#Pull all modmails from the tab you wish
conversations = subreddit.modmail.conversations(state=state)



#For each one, ensure you haven't already replied to it automatically        
for eachConvo in conversations:

    if (eachConvo.id not in mail_replied_to):
        print ("Yes this was not found previously!")
        #Add it to the list before doing any actions 
        mail_replied_to.append(eachConvo.id)
        message = "Super long reply message testing"
        
        #reply also takes 2 optional parameters:
        #internal=true/false <-- Private Mod Note
        #author_hidden=true/false <-- Reply as subreddit
        eachConvo.reply(body=message)
        if (state is not "mod"):
            eachConvo.archive()
        
        
        
with open(fileName, "w") as f:
    for post_id in mail_replied_to:
        f.write(post_id + "\n")
        
        
        
           
    