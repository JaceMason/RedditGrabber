from RedditGrabber import RedditGrabber
from RedditRecorder import RedditRecorder
import time

def calculate_sleep_time(minute):
	minute = minute % 60
	
	#Calculate the seconds the loop should sleep to run at a specific time every hour.
	#We do some convoluted stuff so we don't have to account for date wrapping
	t = time.time()
	t += (3600 - (minute * 60)) #Use inverse of requested minute so that if it is within the current hour, it will be used (not skipped).
	t = time.localtime(t) #t is now within the hour we will use
	
	#Can't edit time_struct directly, so make it a 'list' and back again
	listT = list(t)
	listT[4] = minute
	listT[5] = 0 #seconds
	t = time.struct_time(tuple(listT))
	
	t = time.mktime(t) #Back to epoch for our calculation
	sleepTime = t - time.time()
	return(sleepTime)


if __name__ == "__main__":
	grab = RedditGrabber()
	record = RedditRecorder()
	
	while(1):
		#---LOOP TIMING STUFF---#
		sleepTime = calculate_sleep_time(33)
		print("Next run scheduled for %s" % time.strftime('%Y-%m-%d at %H:%M', time.localtime(time.time() + sleepTime)))
		if(sleepTime > 0):
			time.sleep(sleepTime)
		#---/LOOP TIMING STUFF---#
		
		print("Running reddit grabber!")
		posts = ()
		try:
			posts = grab.get_reddit_posts(20)
		except:
			#Catch all weird selenium errors
			posts = ()
		
		if posts:
			try:
				record.record_posts(posts)
				print("Successfully added records!")
			except TypeError:
				print("Error: Something went wrong with the reddit data formatting")
