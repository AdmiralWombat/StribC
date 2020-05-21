import os.path
from os import path

from pathlib import Path

import pickle

from comments.models import Article
from comments.models import UserCommenter;
from comments.models import Comment

from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime

import sys
import os

print(Path(__file__).parent.parent.parent.parent)

#sys.path.insert(1, 'D:\\Documents\\source\\WebScraping\\WebScraping')
sys.path.append(os.path.join(Path(__file__).parent.parent.parent.parent, 'StribC/WebScraping/WebScraping/'))
import comment


import re



from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    
    def _init(self):
        print("INITIALIZING")
        ospath = os.getenv('LOCALAPPDATA')
        if ospath == None:
            ospath = Path.home()
            self.storage_directory = os.path.join(ospath, '.DCN/WebScraping/')
            self.storage_stats_directory = os.path.join(ospath, '.DCN/WebScraping/Data/')
            self.unix = 1
        else:
            self.storage_directory = os.path.join(ospath, 'DCN\\WebScraping\\')
            self.storage_stats_directory = os.path.join(ospath, 'DCN\\WebScraping\\Data\\')
            self.unix = 0

        self.newArticles = 0
        self.newComments = 0

        #UserCommenter.objects.all().delete()
        #Article.objects.all().delete()
        #Comment.objects.all().delete()

    def add_arguments(self, parser):
        None

    def handle(self, *args, **options):
        print("STARTING")
        self._init()
        self._loadArticles()
        self._saveStats()

    def _saveStats(self):
        print("SAVING STATS FILE")
        filePath = self.storage_stats_directory + "updateDBStats.dat"
        with open(filePath, 'a+') as f:
            f.write(f"{datetime.now()}\tadded {self.newArticles} articles to database, with {self.newComments} new comments\n")

    def _loadArticles(self):
        print("LOADING")
        if (self.unix == 1):
            articleDirectory = self.storage_directory
        else:
            articleDirectory = self.storage_directory + "\\"
        for filename in os.listdir(articleDirectory):
            filepath = articleDirectory + filename
            print(f"\tATTEMPTING TO LOAD {filepath}")
            try:
                with open(filepath, "rb") as f:
                    headComment = pickle.load(f)
            except FileNotFoundError as e:
                print("FILE NOT FOUND")
                continue
            except Exception as e:
                print("ERROR LOADING FILE")
                print(f"ERROR: {e}")
                continue

            self._addToDB(headComment)

    def _addToDB(self, root):
        print("ADDING TO DB")           
        
        print(f"{root.article.url}")
        urlnumber = re.findall(r"startribune.com/.+/([0-9]+)/", root.article.url)

        if (len(urlnumber) > 0):
            try:
                tempArt = Article.objects.get(title=root.article.title, url__contains=urlnumber[0])
                print("\tFound already, updating info")
                tempArt.title = root.article.title
                tempArt.datePosted = root.article.date                                
                tempArt.save()
                article_id = tempArt.id
            except ObjectDoesNotExist as e:
                print(f"\tCouldn't find {root.article.title} with url {urlnumber[0]}")
                newArt = Article.objects.create(title=root.article.title, url=root.article.url, datePosted=root.article.date, numberOfComments='0')                
                print("\tCreating new")
                newArt.save()
                article_id = newArt.id
                self.newArticles += 1
            except Exception as e:
                print("\tERROR FINDING")
                print(e)
                return
        else:
            print("ERROR: Shouldn't be here\n")
            return


  


        #self.newArticle, self.newArticleCreated = Article.objects.get_or_create(title=root.article.title, url=root.article.url, datePosted=root.article.date, numberOfComments='0')
        print("TRAVERSING TREE")
        self._traverse(root, article_id)

    def _traverse(self, nextnode, article_id):
        for node in nextnode.children:
            self._traverse(node, article_id)

        newUser, newUserCreated = UserCommenter.objects.get_or_create(userName=nextnode.username)
        newComment, newCommentCreated = Comment.objects.get_or_create(message=nextnode.text, datePosted=nextnode.date, username=nextnode.username, creator=UserCommenter(id=newUser.id), article=Article(id=article_id))
        if (newCommentCreated):
            self.newComments+=1


        

        
        