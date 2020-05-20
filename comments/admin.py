from django.contrib import admin

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import TreeComment

from .models import Article
from .models import UserCommenter
from .models import Comment

class MyAdmin(TreeAdmin):
    form = movenodeform_factory(TreeComment)

admin.site.register(TreeComment, MyAdmin)
admin.site.register(UserCommenter)
admin.site.register(Article)
admin.site.register(Comment)