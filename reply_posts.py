#!/usr/bin/python3.7
#Removed MySQL info/Subreddit Details for Github Usage
#git install test
import praw
import pdb
import re
import os
import datetime
import time
import mysql.connector

connection = mysql.connector.connect(host='HOSTADDRESS',database='DATABASENAME',user='USERNAME',password='PASSWORD')
# Create the Reddit instance
reddit = praw.Reddit('BOTNAME/PRAW CONFIG')

# Have we run this code before? If not, create an empty list
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []

# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

# Get the top 2 values from our subreddit
subreddit = reddit.subreddit('SUBREDDITNAME')

for submission in subreddit.new(limit=2):
    cursor=connection.cursor()
    addCursor=connection.cursor()
    
    # If we haven't replied to this post before
    if submission.id not in posts_replied_to:
        listStates = [ "[USA-AL]","[USA-AK]","[USA-AR]","[USA-AZ]","[USA-CA]","[USA-CO]","[USA-CT]","[USA-DC]","[USA-DE]",
                       "[USA-FL]","[USA-GA]","[USA-HI]","[USA-ID]","[USA-IL]","[USA-IN]","[USA-IA]","[USA-KS]","[USA-KY]",
                       "[USA-LA]","[USA-ME]","[USA-MD]","[USA-MI]","[USA-MN]","[USA-MO]","[USA-MS]","[USA-MT]","[USA-NE]",
                       "[USA-NV]","[USA-NH]","[USA-NJ]","[USA-NM]","[USA-NY]","[USA-NY]","[USA-NC]", "[USA-ND]","[USA-OH]",
                       "[USA-OK]","[USA-OR]","[USA-PA]","[USA-RI]","[USA-SC]","[USA-SD]","[USA-TN]","[USA-TX]","[USA-UT]",
                       "[USA-VT]","[USA-VA]","[USA-WA]","[USA-WV]","[USA-WI]","[USA-WY]","[CAN]","[GBR]","[AUS]","[GER]"]
        modFilter=submission.author
        body=submission.selftext
        if any(location in submission.title for location in listStates) and ("[H]" in submission.title) and ("[W]" in submission.title):
            if submission.link_flair_css_class == 'orange' and ("imgur.com" not in body and "icloud.com" not in body):
                removalComment = ("Your submission is flagged as a selling post but does not contain a timestamp from imgur.com, please create a new post that follows all posting guidelines"
                                + " including [USA-STATE][H][W] and a timestamp from imgur.com. A *Valid* timestamp includes a note/paper with your username and current date in the same picture as the item you are selling. "
                                + "Do NOT edit your post to include a timestamp, only new posts will be permitted.")
                removed = submission.reply(removalComment)
                removed.mod.distinguish(how="yes",sticky=True)
                submission.mod.remove()
                print("Bot replying to: ", submission.title)
            else:
                user=submission.author
                sql_find_user="select * from trades where name='"+user.name+"'"
                cursor.execute(sql_find_user)
                rowFound=cursor.fetchone()
                myInt=0
                if rowFound== None:
                    sql_add_user="insert into trades values('"+user.name+"','0')"
                    addCursor.execute(sql_add_user)
                    addCursor.close()
                else:
                    myInt=rowFound[1] 
                    cursor.close()
                dt=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(user.created_utc))
                submission.reply("Username: /u/" + user.name + "\n\nJoin date:" 
                            + str(dt) + "\n\nLink karma:"+ str(user.link_karma)
                            + "\n\nComment karma:" + str(user.comment_karma) + "\n\nConfirmed trades:" + str(myInt)
                             + "\n\n\n^^^The ^^^information ^^^above ^^^is ^^^meant ^^^to ^^^help ^^^you ^^^make ^^^decisions ^^^on ^^^the ^^^original ^^^poster ^^^but ^^^by ^^^no ^^^means ^^^does ^^^it ^^^guarantee ^^^a ^^^successful ^^^transaction."
                             + " ^^^Please ^^^exercise ^^^your ^^^own ^^^caution ^^^regarding ^^^new ^^^accounts ^^^or ^^^those ^^^that ^^^want ^^^venmo/PaypalF&F/zelle ^^^and ^^^other ^^^similar ^^^payment ^^^options ^^^that ^^^do ^^^not ^^^offer ^^^protection.")
                print("Bot replying to : ", submission.title)
        elif modFilter.name=='Nobes1990':
            submission.reply("I love you Nobes")

        else:
            removed = submission.reply("Your submission title does not fit the standard posting guidelines, please repost following the [USA-STATE][H] item/money [W] item/money format. Note that State/Providence requirements are only necessary for the USA, you may use [CAN]/[GBR]/[AUS]/[GER] as necessary.")
            removed.mod.distinguish(how="yes",sticky=True)
            submission.mod.remove()
            print("Bot replying to : ", submission.title)

        # Store the current id into our list
        posts_replied_to.append(submission.id)
connection.commit()
# Write our updated list back to the file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")
        
# Close MySQL connection
if (connection.is_connected()):
    connection.close()
    cursor.close()
    

