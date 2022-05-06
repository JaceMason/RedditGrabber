# RedditGrabber
Simple tool made in selenium to grab some posts from Reddit.

# Dependencies:
- Firefox
- Python 3.6+ (Tested in 3.10.4)
   - Selenium (with Mozilla's geckodriver.exe)
   - matplotlib (3.5+)
    
# Use:
The workflow is as follow:
1. Run MonitorReddit.py
   - It will let you know when the next poll will be
   - It will poll Reddit on the 33rd minute of every hour (this can be changed easily by editing calculate_sleep_time(33) in this file)
2. Wait for a successful poll to occur
   - Indicated by "Successfully added records!" on the console
   - Note: There are a few bugs I am still trying to replicate with Selenium timing out depending on the state of Reddit. (See Issue 1). Some polls may not be successful.
3. Run displaygraph.py
