from RedditRecorder import RedditRecorder
import matplotlib.pyplot as matplot

if __name__ == "__main__":
	print("Make sure you have run RedditMonitor.py before running this!")
	hours = 168
	
	recorder = RedditRecorder()
	subredditDict = recorder.get_posts_by_subreddit(hours)
	
	#Calculate the amount of posts per subreddit and put into a list for sorting.
	subredditCount = []
	for subreddit in subredditDict:
		subredditCount.append((len(subredditDict[subreddit]), subreddit))
	
	subredditCount.sort(reverse=True) #Order them greatest to least
	
	subredditCount = subredditCount[0:10] #Top 10 subreddits with most posts.

	#divide the count and subreddit name for plotting
	subnames = [sub[1] for sub in subredditCount]
	subcount = [num[0] for num in subredditCount]
	
	#Create horizontal bar graph
	figure, ax = matplot.subplots()
	bars = ax.barh(subnames, subcount)
	ax.bar_label(bars)#Show number next to bar.

	matplot.tight_layout()#No cutting off labels
	matplot.show()
