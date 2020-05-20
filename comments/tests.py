from django.urls import reverse
from django.urls import resolve
from django.test import TestCase

from .views import home, comments_view, articles_view
from .models import Article

import datetime

class HomeTests(TestCase):
    def setUp(self):
        self.article = Article.objects.create(title='Test Title', numberOfComments=15, datePosted=datetime.date.today())
        url = reverse('home')
        self.response = self.client.get(url)
    
    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_article_page(self):
        article_url = reverse('articles')
        self.assertContains(self.response, 'href="{0}"'.format(article_url))
    
    


class ArticleTests(TestCase):
    def setUp(self):
        Article.objects.create(title='Test Title', numberOfComments=15, datePosted=datetime.date.today())

    def test_article_view_success_status_code(self):
        url = reverse('articles')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

class CommentsTests(TestCase):
    def setUp(self):
        Article.objects.create(title='Test Title', numberOfComments=15, datePosted=datetime.date.today())

    def test_article_view_success_status_code(self):
        url = reverse('comments', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_article_view_not_found_status_code(self):
        url = reverse('comments', kwargs={'pk':99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_articles_url_resolves_board_topics_view(self):
        view = resolve('/articles/1/')
        self.assertEquals(view.func, comments_view)

    def test_article_view_contains_link_back_to_homepage(self):
        article_url = reverse('comments', kwargs={'pk':1})
        response = self.client.get(article_url)
        homepage_url = reverse('articles')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))