from django.db import models
from treebeard.mp_tree import MP_Node

class TreeComment(MP_Node):
    username = models.TextField()
    datePosted = models.DateTimeField(null=True)
    message = models.TextField()

    node_order_by = ['datePosted']

class UserCommenter(models.Model):
    userName = models.TextField()


class Article(models.Model):
    title = models.TextField()
    url = models.URLField(max_length=1000)
    datePosted = models.DateTimeField(null=True)
    numberOfComments = models.IntegerField()
    lastPost = models.DateTimeField(null=True)

class Comment(models.Model):
    message = models.TextField()
    datePosted = models.DateTimeField(null=True)
    username = models.TextField()
    creator = models.ForeignKey(UserCommenter, related_name='comments', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)



