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
reddit = praw.Reddit('BOTNAME/CONFIG')
subreddit=reddit.subreddit('SUBREDDITNAME')

#Finds the user and increments trade count, if does not exist, create a new user in MySQL
def findUser(username):
    sql_find_user="select * from trades where name='"+username+"'"
    cursor=connection.cursor()
    cursor.execute(sql_find_user)
    userRow=cursor.fetchone()
    if userRow==None:
        addToDatabase(username)
        cursor.close()
    else:
        incrementTrades(username)
        cursor.close()
        
#Locate MySQL row and increment their trade count
def incrementTrades(username):
    sql_increment_trade="update trades set confirmed=confirmed+1 where name='"+username+"'"
    print("incremented "+username + " in database")
    cursor=connection.cursor()
    cursor.execute(sql_increment_trade)
    connection.commit()
    updateFlair(username)

#Add a new user into MySQL
def addToDatabase(username):
    sql_add_user="insert into trades values('"+username+"','1')"
    print("added "+username + " to database")
    cursor=connection.cursor()
    cursor.execute(sql_add_user)
    connection.commit()
    updateFlair(username)

#Update User Flair after incrementing/adding to database
def updateFlair(username):
    cursor=connection.cursor()
    sql_get_count="select confirmed from trades where name='"+username+"'"
    cursor.execute(sql_get_count)
    record=cursor.fetchone()
    subreddit.flair.set(username, text="Trades:"+str(record[0]),css_class="")
    
# Have we run this code before? If not, create an empty list
if not os.path.isfile("FILENAME"):
    posts_replied_to = []
    # If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("FILENAME", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))
    
submission = reddit.submission(id="SUBMISSIONID")
for top_level_comment in submission.comments:
    topCheck = top_level_comment.author
    #Base check, if the user deletes their comment then ignore it
    if (topCheck == None):
        continue
    topUser=top_level_comment.author.name
    for second_level_comment in top_level_comment.replies:
        replyUser=second_level_comment.author.name
        if  (second_level_comment.parent_id not in posts_replied_to) and (("confirmed" in second_level_comment.body) or ("Confirmed" in second_level_comment.body)):
            posts_replied_to.append(second_level_comment.parent_id)
            #search for users
            findUser(topUser)
            findUser(replyUser)
            #Give confirmation to users that it worked
            second_level_comment.reply("Added")
            
with open("FILENAME", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")

# Close MySQL connection
if (connection.is_connected()):
    connection.close()
