from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Category, Article, Comment, Favorite

class BlogTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Хищники', slug='carnivores')
        self.article = Article.objects.create(
            title='Тестовая статья',
            content='Содержание',
            category=self.category,
            author=self.user,
        )
        self.client = Client()

    def test_article_creation(self):
        self.assertEqual(Article.objects.count(), 1)

    def test_article_detail_view(self):
        response = self.client.get(f'/article/{self.article.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_article_create_requires_login(self):
        response = self.client.get('/article/create/')
        self.assertEqual(response.status_code, 302)

    def test_comment_creation(self):
        Comment.objects.create(
            article=self.article,
            user=self.user,
            text='Тестовый комментарий'
        )
        self.assertEqual(Comment.objects.count(), 1)

    def test_favorite_creation(self):
        Favorite.objects.create(user=self.user, article=self.article)
        self.assertEqual(Favorite.objects.count(), 1)

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Хищники')
