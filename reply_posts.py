#!/usr/bin/python3.7
#Removed MySQL info/Subreddit Details for Github Usage

import praw
import pdb
import re
import os
import datetime
import time
import mysql.connector

connection = mysql.connector.connect(host='HOSTADDRESS',database='DATABASENAME',user='USERNAME',password='PASSWORD')
reddit = praw.Reddit('BOTNAME/PRAW CONFIG')
subreddit = reddit.subreddit('SUBREDDITNAME')
fileName="fileName"
removalComment = ("Your submission is flagged as a selling post but does not contain a timestamp from imgur.com, please create a new post that follows all posting guidelines"
                                + " including [USA-STATE][H][W] and a timestamp from imgur.com. A *Valid* timestamp includes a note/paper with your username and current date in the same picture as the item you are selling. "
                                + "Do NOT edit your post to include a timestamp, only new posts will be permitted.")
listStates = ["[USA-AL]","[USA-AK]","[USA-AR]","[USA-AZ]","[USA-CA]","[USA-CO]","[USA-CT]","[USA-DC]","[USA-DE]",
              "[USA-FL]","[USA-GA]","[USA-HI]","[USA-ID]","[USA-IL]","[USA-IN]","[USA-IA]","[USA-KS]","[USA-KY]",
              "[USA-LA]","[USA-ME]","[USA-MD]","[USA-MI]","[USA-MN]","[USA-MO]","[USA-MS]","[USA-MT]","[USA-NE]",
              "[USA-NV]","[USA-NH]","[USA-NJ]","[USA-NM]","[USA-NY]","[USA-NY]","[USA-NC]", "[USA-ND]","[USA-OH]",
              "[USA-OK]","[USA-OR]","[USA-PA]","[USA-RI]","[USA-SC]","[USA-SD]","[USA-TN]","[USA-TX]","[USA-UT]",
              "[USA-VT]","[USA-VA]","[USA-WA]","[USA-WV]","[USA-WI]","[USA-WY]","[CAN]","[GBR]","[AUS]","[GER]","[USA-MA]","[CHE]"]


def findUser(username):
    sql_find_user = "select * from trades where name='"+username+"'"
    cursor=connection.cursor()

    cursor.execute(sql_find_user)
    rowFound=cursor.fetchone()
    if (rowFound==None):
        addUser(username)
        cursor.close()
        return 0
    else:
        sql_user_posted = "update trades set posted = 1 where name ='"+username+"'"
        editCursor=connection.cursor()
        editCursor.execute(sql_user_posted)
        editCursor.close()
        return rowFound[1]
      

    
def addUser(username):
    addCursor=connection.cursor()
    sql_add_user="insert into trades values('"+username+"',0,1)"
    subreddit.flair.set(username, text="Trades:0",css_class="")
    addCursor.execute(sql_add_user)
    addCursor.close()

# Have we run this code before? If not, create an empty list
if not os.path.isfile(fileName):
    posts_replied_to = []

# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open(fileName, "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

# Get the top 2 values from our subreddit, as low activity 

for submission in subreddit.new(limit=2):

    # If we haven't replied to this post before
    if submission.id not in posts_replied_to:
        
        user=submission.author.name
        body=submission.selftext
        if any(location in submission.title for location in listStates) and ("[H]" in submission.title) and ("[W]" in submission.title):
            if submission.link_flair_css_class == 'orange' and ("imgur.com" not in body and "icloud.com" not in body):
               
                removed = submission.reply(removalComment)
                removed.mod.distinguish(how="yes",sticky=True)
                submission.mod.remove()
                # print("Bot replying to: ", submission.title)  #debugging
            else:
                myTrades=findUser(user)
                #Convert to user friendly date
                dt=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(submission.author.created_utc))
                submission.reply("Username: /u/" + user + "\n\nJoin date:" 
                            + str(dt) + "\n\nLink karma:"+ str(submission.author.link_karma)
                            + "\n\nComment karma:" + str(submission.author.comment_karma) + "\n\nConfirmed trades:" + str(myTrades)
                             + "\n\n\n^^^The ^^^information ^^^above ^^^is ^^^meant ^^^to ^^^help ^^^you ^^^make ^^^decisions ^^^on ^^^the ^^^original ^^^poster ^^^but ^^^by ^^^no ^^^means ^^^does ^^^it ^^^guarantee ^^^a ^^^successful ^^^transaction."
                             + " ^^^Please ^^^exercise ^^^your ^^^own ^^^caution ^^^regarding ^^^new ^^^accounts ^^^or ^^^those ^^^that ^^^want ^^^venmo/PaypalF&F/zelle ^^^and ^^^other ^^^similar ^^^payment ^^^options ^^^that ^^^do ^^^not ^^^offer ^^^protection.")
               #print("Bot replying to : ", submission.title) #debug
        elif user=='Nobes1990' or user=='ItzADino' or user=='Moomius':
            continue; # Mods are exempt from any filtering

        else:
            removed = submission.reply("Your submission title does not fit the standard posting guidelines, please repost following the [USA-STATE][H] item/money [W] item/money format. Note that State/Providence requirements are only necessary for the USA, you may use [CAN]/[GBR]/[AUS]/[GER] as necessary.")
            removed.mod.distinguish(how="yes",sticky=True)
            submission.mod.remove()
           # print("Bot replying to : ", submission.title) #debugging

        # Store the current id into our list
        posts_replied_to.append(submission.id)
        
connection.commit()
# Write our updated list back to the file
with open(fileName, "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")
        
# Close MySQL connection
if (connection.is_connected()):
    connection.close()
    
    

