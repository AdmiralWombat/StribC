"""StribC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from comments import views

urlpatterns = [
    url(r'^$', views.home, name='home'),        
    #url(r'^comments/(?P<pk>\d+)/$', views.comments_view, name='comments'),
    url(r'^articles/(?P<pk>\d+)/$', views.articles_view, name='articles'), 
    url(r'^articles/(?P<pk>\d+)/comments/(?P<comment_pk>\d+)/$', views.comments_view, name='comments'),
    url(r'^about/$', views.about_view, name='about'),
    url(r'^admin/', admin.site.urls),

]
