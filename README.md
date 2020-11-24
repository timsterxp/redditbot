# redditbot
A simple Python-based Reddit bot for moderators in transaction-based subreddits. Includes automated filtering rules, more detailed user information, and also MySQL usage to track and update transaction amounts. 

reply_post.py
  Checks the given subreddit for new posts and has filtering rules to ensure all posts meet posting guidelines. If so, user information is taken to provide other users information about the original poster such as time of creation of account, karma counts, trades the user has done as well as a reminder to exercise safety when doing online-transactions. If not, the user is informed of why and how they can fix their post.
  
 confirm_trade.py
  Checks a given post (E.g. a confirmed thread), where users can post about successful transactions with other users. If the other user confirms the success of the trade, their trade count is incremented in MySQL and updated on user flairs.
  
 To ensure high uptime, these are ran under a Google Cloud engine utilizing crontab -e every minute. Furthermore, Google Cloud MySQL was also used for the simplicity and easy back ups.
 
 Project Future Goals: 
 - Add a user check for confirmed trades to lower the potential of people doing "false" confirmations
 - Create  a limit for posting for when the subreddit reaches a certain size
 - Potentially move over to a physical location (e.g. Raspberry Pi's) in terms of cost effiency and long-term usage
 - Refractoring code as necessary to fit Python and OOD/OOP guidelines and for better readability
