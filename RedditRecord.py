import sqlite3
from datetime import datetime, timezone
import os

class RedditRecorder:
    def raise_type_error(self, message):
        raise TypeError(message + " Data must be in the form of [(<int>, <str>, <str>), ...]")
    
    def record_posts(self, dataTupleList):
        '''
        Incoming data must be a list of tuples with the following structure:
        
        (<int>, <str>, <str>)
        (postRank, subreddit, headline)
        
        Check for this.
        '''
        #must be list
        if not isinstance(dataTupleList, list):
            self.raise_type_error("Incoming data was not a list.")
        
        for listEntryIndex, listEntry in enumerate(dataTupleList):
            #All list entries must be tuples
            if not isinstance(listEntry, tuple):
                    self.raise_type_error("List entry %d must be tuple." % listEntryIndex)
            #tuples must have length 3
            if len(listEntry) != 3:
                self.raise_type_error("List entry %d was of size %d." % (listEntryIndex, len(listEntry)))
            #must be in the form (<int>, <str>, <str>)
            if not isinstance(listEntry[0], int):
                    self.raise_type_error("List entry %d, tuple entry %d." % (listEntryIndex, 0))
            if not isinstance(listEntry[1], str):
                    self.raise_type_error("List entry %d, tuple entry %d." % (listEntryIndex, 1))
            if not isinstance(listEntry[2], str):
                    self.raise_type_error("List entry %d, tuple entry %d." % (listEntryIndex, 2))
        
        database = sqlite3.connect('redditlog.db')
        
        cur = database.cursor()
        
        #Initialize the database
        cur.execute("PRAGMA foreign_keys = ON;")
        cur.execute('''
            CREATE TABLE IF NOT EXISTS polls(
                poll_id INTEGER PRIMARY KEY,
                poll_time REAL)
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS posts(
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
        dataList = [(newRow,) + tupl for tupl in dataTupleList]
        
        cur.executemany("INSERT INTO posts VALUES (?, ?, ?, ?)", dataList)
        
        database.commit()
        database.close()

if __name__ == "__main__":
    blah = RedditRecorder()
    
    goodData = [(1, "r/test", "Headline"), (2, "r/exam", "Highlight"), (3, "r/assessment", "Summary")]
    blah.record_posts(goodData)

    #couple quick tests for the type errors.
    print("Testing for poorly structured input data:")
    badDataList = [
        "Hello",
        ["Hello"],
        [("Hello")],
        [("Hello", 1, "Uh.")],
        [(1, 2, "Hello")],
        [(1, "Hello", 2.2)],
        [(1, "r/Hello", "2.2"), (3, "r/Hi", 1)]
    ]
    for i, badData in enumerate(badDataList):
        try:
            blah.record_posts(badData)
            print("Uh oh. Test %d failed to fail" % i)
        except TypeError:
            print("Test %d failed successfully" % i)
