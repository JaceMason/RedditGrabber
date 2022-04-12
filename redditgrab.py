from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

import time

if __name__ == "__main__":

    numPostsToGrab = 30
    options = Options()
    #options.headless = True
    driver = webdriver.Firefox(options = options)

    redditPostClass = "_1oQyIsiPHYt6nx7VOmd1sz"
    redditHdrClass = "_eYtD2XCVieq6emjKBH3m"
    subredditClass = "_2mHuuvyV9doV3zwbZPtIPG"
    adClass = "_2oEYZXchPfHwcf9mTMGMg8"
    
    driver.get("https://www.reddit.com")

    #To deal with infinite scrolling, we keep going to the bottom of the page until we have all our posts.
    postsOnScreen = 0
    while postsOnScreen < numPostsToGrab:
        posts = driver.find_elements_by_class_name(redditPostClass)
        postsNoAds = [p for p in posts if not p.find_elements_by_class_name(adClass)]
        postsOnScreen = len(postsNoAds)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(postsNoAds[-1], 20).until(EC.visibility_of_element_located((By.CLASS_NAME, redditHdrClass)))

    #Out of site elements are usually set to display:none, so we need to scroll to the top to interact with them.
    driver.execute_script("window.scrollTo(0, 0);")
    
    for post in postsNoAds[:numPostsToGrab]:
        driver.execute_script("arguments[0].scrollIntoView();", post)
        headline = WebDriverWait(post, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, redditHdrClass)))
        subreddit = WebDriverWait(post, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, subredditClass)))
        print("%s: %s"%(subreddit.text, headline.text))
        
    driver.quit()
