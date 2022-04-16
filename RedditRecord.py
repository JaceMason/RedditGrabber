import sqlite3
from datetime import datetime, timezone
import os
from redditgrab import RedditGrabber

#Debug
try:
    os.remove("redditlog.db")
except:
    pass
#/Debug

grabber = RedditGrabber()

posts = grabber.get_reddit_posts(25)

database = sqlite3.connect('redditlog.db')

cur = database.cursor()

#Initialize the database
cur.execute("PRAGMA foreign_keys = ON;")
cur.execute('''
    CREATE TABLE polls(
        poll_id INTEGER PRIMARY KEY,
        poll_time REAL)
''')

cur.execute('''
    CREATE TABLE posts(
        post_poll INTEGER,
        post_rank INTEGER,
        subreddit TEXT,
        headline TEXT,
        FOREIGN KEY(post_poll) REFERENCES polls(poll_id))
''')

#insert some values
cur.execute('''
    INSERT INTO polls (poll_time)
    VALUES(%f)'''
    % datetime.utcnow().timestamp()
)

newRow = cur.lastrowid
dbTupleList = [(newRow,) + tupl for tupl in posts]

cur.executemany("INSERT INTO posts VALUES (?, ?, ?, ?)", dbTupleList)

database.commit()

