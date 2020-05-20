import os.path
from os import path

import pickle

from comments.models import Article
from comments.models import UserCommenter;
from comments.models import Comment

from django.core.exceptions import ObjectDoesNotExist

import sys

sys.path.insert(1, 'D:\\Documents\\source\\WebScraping\\WebScraping')

import comment

import re



from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    
    def _init(self):
        print("INITIALIZING")
       
       # UserCommenter.objects.all().delete()
       # Article.objects.all().delete()
       # Comment.objects.all().delete()

        self.storage_directory = os.path.join(os.getenv('LOCALAPPDATA'), 'DCN\\WebScraping\\')

    def add_arguments(self, parser):
        None

    def handle(self, *args, **options):
        print("STARTING")
        self._init()
        self._loadArticles()

    def _loadArticles(self):
        print("LOADING")
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
        urlnumber = re.findall(r"https://www.startribune.com/.+/([0-9]+)/", root.article.url)        

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
            except Exception as e:
                print("\tERROR FINDING")
                print(e)



  


        #self.newArticle, self.newArticleCreated = Article.objects.get_or_create(title=root.article.title, url=root.article.url, datePosted=root.article.date, numberOfComments='0')
        print("TRAVERSING TREE")
        self._traverse(root, article_id)

    def _traverse(self, nextnode, article_id):
        for node in nextnode.children:
            self._traverse(node, article_id)

        newUser, newUserCreated = UserCommenter.objects.get_or_create(userName=nextnode.username)
        Comment.objects.get_or_create(message=nextnode.text, datePosted=nextnode.date, username=nextnode.username, creator=UserCommenter(id=newUser.id), article=Article(id=article_id))       



        

        
        