from django.db import models
from treebeard.mp_tree import MP_Node

class Category(MP_Node):
    name = models.TextField()
    date = models.DateTimeField(null=True)
    
