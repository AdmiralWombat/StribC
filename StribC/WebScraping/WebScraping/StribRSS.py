import feedparser

from datetime import datetime, timedelta
import dateutil.parser
from dateutil.tz import tzutc

import os.path
from os import path
from pathlib import Path

from article import Article

import pickle

class StribCRSSParse:
    def __init__(self):
        print("INITIALIZING")
        ospath = os.getenv('LOCALAPPDATA')

        self.count = 0

        if ospath == None:
            ospath = Path.home()
            self.storage_directory = os.path.join(ospath, '.DCN/WebScraping/Data')
            Path(self.storage_directory).mkdir(parents=True, exist_ok=True)
            filePath = self.storage_directory + "/RSSArticleFeed.dat"
            statsFilePath = self.storage_directory + "/RSSArticleFeedStats.dat"
        else:
            self.storage_directory = os.path.join(ospath, 'DCN\\WebScraping\\Data')
            Path(self.storage_directory).mkdir(parents=True, exist_ok=True)
            filePath = self.storage_directory + "\\RSSArticleFeed.dat"
            statsFilePath = self.storage_directory + "/RSSArticleFeedStats.dat"

        self.twoWeeksAgo = datetime.now() - timedelta(days=14)
        self.twoWeeksAgo = self.twoWeeksAgo.replace(tzinfo=tzutc())

        self.articleSet = set()

        self._loadArticleFile(filePath)

        self._loadRSSFeed('https://www.startribune.com/rss/?sf=1&s=/')
        self._loadRSSFeed('https://www.startribune.com/local/index.rss2')
        self._loadRSSFeed('https://www.startribune.com/sports/index.rss2')
        self._loadRSSFeed('https://www.startribune.com/business/index.rss2')
        self._loadRSSFeed('https://www.startribune.com/politics/index.rss2')
        self._loadRSSFeed('https://www.startribune.com/opinion/index.rss2')
        self._loadRSSFeed('https://www.startribune.com/variety/index.rss2')

        self._cleanArticleSet()

        self._saveArticleFile(filePath)

        self._saveStatsFile(statsFilePath)

  
    def _cleanArticleSet(self):
        print("REMOVING OLD ARTICLES")                 
        newArticleSet = set()
        for article in self.articleSet:
            if (article.date > self.twoWeeksAgo):
                newArticleSet.add(article)  
        self.articleSet = set(newArticleSet)

    
    def _loadArticleFile(self, filePath):
        print("LOADING ARTICLE FILE")
        try:
            with open(filePath, 'rb') as f:
                self.articleSet = pickle.load(f)    
        except FileNotFoundError as e:
            print(e)
            return


    def _loadRSSFeed(self, rss_url):
        print(f"PARSING: {rss_url}")
        feed = feedparser.parse(rss_url)
        for entry in feed.entries:
            dateparsed = dateutil.parser.isoparse(entry.updated)
            newArticle = Article(entry.title, dateparsed, entry.link)
            inSet = newArticle in self.articleSet
            if inSet:
                self.articleSet.remove(newArticle)
                self.count-=1
            self.articleSet.add(newArticle)
            self.count+=1
            
    def _saveArticleFile(self, filePath):
        print("SAVING")           

        with open(filePath, 'wb') as f:            
            pickle.dump(self.articleSet, f)

    def _saveStatsFile(self, filePath):
        print("SAVING STATS")

        with open(filePath, 'a+') as f:
            f.write(f"{datetime.now()}\tsaved {self.count} new articles in RSS file\n")
            

     
cParse = StribCRSSParse()
