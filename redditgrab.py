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

    
    skipAds = True
    postsOnScreen = 0
    lastPost = 0
    textPosts = []
    while postsOnScreen < numPostsToGrab:
        posts = driver.find_elements_by_class_name(redditPostClass)
        while lastPost < len(posts):
            #To deal with infinite scrolling, we need to scroll to the new posts as they appear (or to the bottom)
            driver.execute_script("arguments[0].scrollIntoView();", posts[lastPost])

            #Do not include ads in the collected posts if requested.
            if not posts[lastPost].find_elements_by_class_name(adClass) and skipAds:
                headline = WebDriverWait(posts[lastPost], 20).until(EC.visibility_of_element_located((By.CLASS_NAME, redditHdrClass)))
                subreddit = WebDriverWait(posts[lastPost], 20).until(EC.visibility_of_element_located((By.CLASS_NAME, subredditClass)))            
                textPosts.append((headline.text, subreddit.text))

            lastPost += 1
                
        postsOnScreen = len(textPosts)
        WebDriverWait(posts[-1], 20).until(EC.visibility_of_element_located((By.CLASS_NAME, redditHdrClass)))

    for text in textPosts:
        print(text);
    
    driver.quit()
