from django.shortcuts import render, redirect, get_object_or_404

from .models import Comment
from .models import Article
from .models import TreeComment
from .models import UserCommenter

import collections

import sys

from datetime import datetime

def home(request):

    if request.method == 'POST':
        find = request.POST['username']         
        commenter = UserCommenter.objects.get(userName__iexact=find)
        return redirect('articles', commenter.id)

    return render(request, 'home.html')

def about_view(request):
    return render(request, 'about.html')

def comments_view(request, pk, comment_pk):    
    article = Article.objects.get(id=comment_pk)   
    comments = Comment.objects.filter(creator=pk, article=comment_pk)

    return render(request, 'comments.html', {'comments' : comments, 'article' : article, 'back' : pk})

def articles_view(request, pk):
    username = UserCommenter.objects.get(pk=pk).userName
    articles = Article.objects.filter(comments__creator__userName=username).order_by('datePosted').distinct()
   
    #unique_articles = articles.distinct()


    for article in articles:
        comments = (Comment.objects.filter(creator=pk, article=article.pk))
        article.numberOfComments = comments.count()
        if comments.count() > 0:
            lastpost = comments[0].datePosted
            for comment in comments:
                if (comment.datePosted > lastpost):
                    lastpost = comment.datePosted

            article.lastPost = lastpost



    return render(request, 'articles.html', {'articles' : articles, 'commenter_name' : username, 'commenter' : pk})
   

