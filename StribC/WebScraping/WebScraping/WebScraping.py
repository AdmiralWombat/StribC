from selenium import webdriver      
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementNotSelectableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException

import time
from pytz import timezone
import pytz

from datetime import datetime, date, timedelta

from article import Article
from comment import Comment 

import hashlib
import os.path
from os import path

from pathlib import Path

import re

import pickle

class WebScrapping:
    def __init__(self):
        print("Initializing")

        ospath = os.getenv('LOCALAPPDATA')
        if ospath == None:
            ospath = Path.home()
            self.storage_directory = os.path.join(ospath, '.DCN/WebScraping/')
            Path(self.storage_directory).mkdir(parents=True, exist_ok=True)
            self.storage_data_directory = os.path.join(ospath, '.DCN/WebScraping/Data/')
            Path(self.storage_data_directory).mkdir(parents=True, exist_ok=True)
            self.rssfilePath = self.storage_data_directory + "RSSArticleFeed.dat"
            self.statsFilePath = self.storage_data_directory + "WebScrapping.dat"
        else:
            self.storage_directory = os.path.join(ospath, 'DCN\\WebScraping\\')
            Path(self.storage_directory).mkdir(parents=True, exist_ok=True)
            self.storage_data_directory = os.path.join(ospath, 'DCN\\WebScraping\\Data\\')
            Path(self.storage_data_directory).mkdir(parents=True, exist_ok=True)
            self.rssfilePath = self.storage_data_directory + "\\RSSArticleFeed.dat"
            self.statsFilePath = self.storage_data_directory + "WebScrapping.dat"

        PATIENCE_TIME = 60

        self.parseCount = 0
        self.commentsSaved = 0

    def start(self):
        print("Running")

        startTime = time.perf_counter()
               
        try:
            self.driver = webdriver.Chrome()
        except:
            self.driver = webdriver.Chrome(executable_path='D:\\Documents\\chromedriver_win32\\chromedriver.exe')

        self.rssArticleSet = set()

        self._loadRSSArticleSet(self.rssfilePath)
        i=0
        #for article in self.rssArticleSet:
         #  self._parseArticle(article.url)
         #  self.parseCount+=1
           #i+=1
           #if (i > 4):
           #    break

        #self._parseArticle('https://www.startribune.com/pazzaluna-restaurant-closes-after-a-21-year-run-in-downtown-st-paul/570539422/')

        #self._parseArticle('https://www.startribune.com/minnesota-covid-19-cases-jump-by-786-with-23-more-deaths/570276032/')
        #self._parseArticle('https://www.startribune.com/wisconsin-bars-and-businesses-quickly-reopen-for-now/570471942/')
        #self._parseArticle('https://www.startribune.com/metro-transit-to-require-face-coverings-on-buses-trains/570513542/')

        self._parseArticle('https://www.startribune.com/minnesota-state-fair-canceled-due-to-covid-19/570694142/')
        
        #time.sleep(10)

        endTime = time.perf_counter()
        totalTime = endTime - startTime

        print("Finished")
        print(f"Took {totalTime} seconds" )
        self.driver.quit()

        self._saveStatsFile(self.statsFilePath)

    def _saveStatsFile(self, filePath):
        print("SAVING STATS FILE")

        with open(filePath, 'a+') as f:
            f.write(f"{datetime.now()}\tAttempted to parse {self.parseCount} articles and saved {self.commentsSaved} new comments\n")


    def _loadRSSArticleSet(self, filePath):
        print("LOADING ARTICLE FILE")
        with open(filePath, 'rb') as f:
            self.rssArticleSet = pickle.load(f)  

    def _waitForLoad(self, driver, inputXPath, waittime): 

        Wait = WebDriverWait(driver, waittime)       

        try:
            Wait.until(EC.presence_of_element_located((By.XPATH, inputXPath)))
        except TimeoutException as e:
            print(e)
            return

 

    def _loadWebPage(self, url):
        self.driver.get(url)
        print("Got URL, waiting for headline to load...")
        self._waitForLoad(self.driver, '//*[contains(@class, "article-headline")]', 10)
        try:
            self.article_title = self.driver.find_element_by_xpath('//*[contains(@class, "article-headline")]').text
            self.article_date = self.driver.find_element_by_xpath('//*[@class="article-dateline"]').text
            print("Got title/date, waiting on comment src to load")
            self._waitForLoad(self.driver, '//*[@id="news_talk_stream_iframe"]', 30)
            comment_src = self.driver.find_element_by_xpath('//*[@id="news_talk_stream_iframe"]').get_attribute("src")
        except NoSuchElementException as e:
            print(e)
            return        
        print("Got comment src, loading comment src url");
        self.driver.get(comment_src)

    def _loadMoreComments(self):
        while True:
            try:
      
                #loadMoreButton = self.driver.find_element_by_xpath('//*[@id="stream"]/div[3]/div[2]/div/div/div/div/div[3]/button')
                loadMoreButton = self.driver.find_element_by_xpath('//button[contains(text(),"show more comments")]')
                #loadMoreButton = self.driver.find_element_by_xpath('//button[contains(@class,"talk-load-more")]')
                #time.sleep(1)                                                       
        
                loadMoreButton.click()
                time.sleep(.1)
            except Exception as e:
                print(e)
                break

    def _showMoreReplies(self):
        try:
            commentsContainer = self.driver.find_element_by_xpath("//div[@class='talk-stream-comments-container']/div")
        except Exception as e:
            print(e)

        while True:
            try:
                AllLoadMoreButtons = commentsContainer.find_elements_by_xpath("//button[contains(text(),'Show more replies')]")
                showMoreTimes = 0
                for loadMoreButton in AllLoadMoreButtons:
                    try:
                        #if loadMoreButton.text == 'SHOW MORE REPLIES':
                        loadMoreButton.click()
                        showMoreTimes += 1
                    except ElementNotInteractableException as e:
                        print(e)
                    except ElementNotSelectableException as e:
                        print(e)
                    except ElementClickInterceptedException as e:
                        print(e)
            
                if showMoreTimes == 0:
                    break

           
                time.sleep(.1)
            except Exception as e:
                print(e)
                break

    def _buildComments(self, elements, parent):
        for comment in elements:
            header = comment.find_element_by_xpath("./div/div/div/div[contains(@class, 'Comment__header')]")        
            content = comment.find_element_by_xpath("./div/div/div/div[contains(@class, 'Comment__content')]")
            username = header.find_element_by_xpath("./div/div[contains(@class, 'Comment__username')]")
            date = header.find_element_by_xpath("./div/span[contains(@class, 'Comment__bylineSecondary')]")
        
            todayyear = datetime.now().year
            todayday = datetime.now().day
            todaymonth = datetime.now().month
            try:
                dt = datetime.strptime(date.text, '%B %d')
            
                dt = dt.replace(year=todayyear)
            except Exception as e:
                try:
                    dt = datetime.strptime(date.text, '%I:%M%p')
                    dt = dt.replace(year=todayyear, month=todaymonth, day=todayday)
                except Exception as e2:
                    try:
                        dt = datetime.strptime(date.text, '%M MINUTES AGO')
                        dt = datetime.now() - timedelta(minutes=dt.minute)                       
                    except Exception as e3:
                        print("Issue formatting date")
                        print(e3)
                        dt = datetime.now()
        
            central = timezone('US/Central')
            dt = dt.replace(tzinfo=central)

            newComment = Comment(username.text, dt, content.text, None, parent)

            commentAgain = comment.find_elements_by_xpath("./span/div")
            self._buildComments(commentAgain, newComment)

            if (newComment not in parent.children):
                self.commentsSaved+=1
                parent.children.append(newComment)

    def _parseArticle(self, url):
        print("Loading webpage");
        self._loadWebPage(url)
        time.sleep(1);
        print("Beginning to expand comments");
        self._loadMoreComments()
        print("Finished showing more")
        self._showMoreReplies()
        print('Done Expanding More')
        #time.sleep(2)

        hash_object = hashlib.md5(url.encode())

        
        todayyear = datetime.now().year
        todayday = datetime.now().day
        todaymonth = datetime.now().month      

        formatDate = '%B %d, %Y ' + chr(8212) + ' %I:%M%p'
        #self.article_date = 'MAY 8, 2020 '
        #formatDate = '%B %d, %Y'
        try:
            dt = datetime.strptime(self.article_date, formatDate)            
        except Exception as e:        
            print("Issue formatting date")
            print(e)
            dt = datetime.now()
        central = timezone('US/Central')
        dt = dt.replace(tzinfo=central)       

        today = datetime.now()
        today = today.replace(tzinfo=central)
        week_ago = today - timedelta(days=7)

        if (dt < week_ago):
            print("Article is too old, skipping")
            return

        newArticle = Article(self.article_title, dt, url)


        headComment = Comment('', None, '', newArticle, None)

        filePath = self.storage_directory + "\\" + hash_object.hexdigest()

        try:
            with open(filePath, "rb") as f:
                headComment = pickle.load(f)
        except FileNotFoundError:
            None
        except:
            None

        try:
            commentsContainer = self.driver.find_element_by_xpath("//div[@class='talk-stream-comments-container']")
            commentsFound = commentsContainer.find_elements_by_xpath("./div/div")
        except NoSuchElementException as e:
            print(e)
            return

        try:
            self._buildComments(commentsFound, headComment)
        except Exception as e:
            print(e)

        #time.sleep(2)

        self._saveArticle(filePath, headComment)

        #self._buildDjangoTree()

    def _saveArticle(self, filePath, root):
        print("Saving")      

        with open(filePath, 'wb') as f:
            pickle.dump(root, f)

    def _buildDjangoTree(self):
        print("Building Tree")


wb = WebScrapping() 
wb.start()
