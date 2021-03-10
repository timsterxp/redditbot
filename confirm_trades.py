#!/usr/bin/python3.7
#Removed MySQL info/Subreddit Details for Github Usage/File Example

import praw
import pdb
import re
import os
import datetime
import time
import mysql.connector

connection = mysql.connector.connect(host='HOSTADDRESS',database='DATABASENAME',user='USERNAME',password='PASSWORD')
submission = reddit.submission(id='SUBMISSIONID')
subreddit=reddit.subreddit('SUBREDDITNAME')
reddit = praw.Reddit('BOTNAME/CONFIG')
fileName="filename.txt"

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
    sql_add_user="insert into trades(name,confirmed) values('"+username+"','1')"
    print("added "+username + " to database")
    cursor=connection.cursor()
    cursor.execute(sql_add_user)
    connection.commit()
    updateFlair(username)

#Update User flair after incrementing/adding to database
def updateFlair(username):
    cursor=connection.cursor()
    sql_get_count="select confirmed from trades where name='"+username+"'"
    cursor.execute(sql_get_count)
    record=cursor.fetchone()
    subreddit.flair.set(username, text="Trades:"+str(record[0]),css_class="")
    
def checkUsers(userOne,userTwo):
    cursor=connection.cursor()
    sql_check_users="select posted from trades where name ='"+userOne+"' or name='"+userTwo+"'"
    cursor.execute(sql_check_users)
    userList=cursor.fetchall()
    valNeeded =0;
    for val in userList:
        valNeeded+=val[0]
    return valNeeded


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
    
#Go through all comments in the thread
for top_level_comment in submission.comments:
    topCheck = top_level_comment.author
    
    #Base check, if the user deleted their comment then ignore it 
    if (topCheck == None):
        continue
    
    topUser=top_level_comment.author.name
    for second_level_comment in top_level_comment.replies:
        if(second_level_comment.author==None):
            continue
        replyUser=second_level_comment.author.name
        
        if  (second_level_comment.parent_id not in posts_replied_to) and (("confirmed" in second_level_comment.body) or ("Confirmed" in second_level_comment.body)):
            #User replying must have been tagged in original comment
            
            if (replyUser.lower() in top_level_comment.body.lower()):
                posts_replied_to.append(second_level_comment.parent_id)
                #Ensure that at least one of the users had posted in the past month
                #if checkUsers(topUser,replyUser)!=0:
                     #search for users
                findUser(topUser)
                findUser(replyUser)
                #Give confirmation to users that it worked
                second_level_comment.reply("Added")
                #else:
                #   top_level_comment.reply("There was an issue adding, paging /u/ItzADino")
with open(fileName, "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")

# Close MySQL connection
if (connection.is_connected()):
    connection.close()
