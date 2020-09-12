from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import date
from datetime import datetime
from datetime import timedelta
import time
import csv
import re

PATH = "C:/Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(PATH)

def recent_10_posts(username):
    url = "https://www.instagram.com/" + username + "/"
    browser = webdriver.Chrome(PATH)
    browser.get(url)
    post = 'https://www.instagram.com/p/'
    post_links = []
    while len(post_links) < 10:
        links = [a.get_attribute('href') for a in browser.find_elements_by_tag_name('a')]
        for link in links:
            if post in link and link not in post_links:
                post_links.append(link)
        scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
        browser.execute_script(scroll_down)
    else:
        return post_links[:25]

def deEmojify(text):
    """
    Removes all emojis from a string
    Update if encounter unpatterned emoji
    """
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U0001f9e0"             #brain character
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

def findNumbers(text):
    """Finds first number in the string as an int"""
    return int(re.search(r'\d+', text).group())

def toTimeDeltaHours(number):
    """Converts a given number of "hours ago" to a timedelta"""
    return timedelta(hours = number)

def toTimeDeltaDays(number):
    """Converts a given number of "days ago" to a timedelta"""
    return timedelta(days = number)

def toTimeDeltaWeeks(number):
    """Converts a given number of "weeks ago" to a timedelta"""
    return timedelta(days = number * 7)

def toDate(time_difference):
    """
    Takes a time difference and returns the correct date
    time_difference MUST be string
    """
    current_date = datetime.now()
    if "HOURS AGO" in time_difference:
        hours_ago = toTimeDeltaHours( findNumbers( time_difference) ) #creates timedelta object of how many hours ago
        correct_date = current_date - hours_ago 

    if "DAYS AGO" in time_difference:
        days_ago = toTimeDeltaDays( findNumbers( time_difference) ) #creates timedelta object of how many days ago
        correct_date = current_date - days_ago

    if "w" in time_difference:
        weeks_ago = toTimeDeltaWeeks( findNumbers( time_difference)) #creates timedelta object of how many weeks ago
        correct_date = current_date - weeks_ago 

    return correct_date


def insta_details(urls):
    """Take a post url and return post details"""
    browser = webdriver.Chrome(PATH)
    browser.maximize_window()
    post_details = []
    for link in urls:
        browser.get(link)
        try:
            #videoLikes = browser.find_elements_by_class_name("_690y5")
            videoViews = browser.find_element_by_class_name("vcOH2").text
            scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
            browser.execute_script(scroll_down)
            browser.find_element_by_class_name("vcOH2").click()
            xpath_view = '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div/div[4]/span'
            videoLikes = browser.find_element_by_xpath(xpath_view).text
            PicturePostlikes = 0
        except:
            PicturePostlikes = browser.find_element_by_class_name("Nm9Fw").text
            videoViews = 0
            videoLikes = 0
        
        time = browser.find_element_by_css_selector('a time').text #gets the time on the post 
        if ("w" in time): #due to inaccuracy in delta time due to instagram data provided, the time can only be determined up to week of 
            date = toDate(time)
            time = "week of " + date.strftime('%B').upper() + " " + str(date.day)

        if ("HOURS AGO" in time) or ("DAYS AGO" in time): #if the time is in "HOURS AGO", "DAYS AGO", or "w", converts it to a date
            date = toDate(time)
            time = date.strftime('%B').upper() + ' ' + str(date.day)
        

        title = deEmojify(browser.title[25:]) #gets the title of post and removes emojis and removes beginning
        
        post_details.append({"title":title,"Video Likes":videoLikes,"Video Views":videoViews,"Picture Post Likes":PicturePostlikes,"time":time})
    
    keys = post_details[0].keys()
    
    with open("data.csv","w",newline = '') as csvfile: #writes data into csv file
        dict_writer = csv.DictWriter(csvfile, keys)
        dict_writer.writeheader()
        dict_writer.writerows(post_details)

        

insta_details(recent_10_posts("scale.scape"))
#print(insta_details(recent_10_posts("scale.scape")))