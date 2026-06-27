from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('article/create/', views.article_create, name='article_create'),
    path('article/<int:pk>/edit/', views.article_edit, name='article_edit'),
    path('article/<int:pk>/delete/', views.article_delete, name='article_delete'),
    path('article/<int:pk>/favorite/', views.favorite_add, name='favorite_add'),
    path('article/<int:pk>/unfavorite/', views.favorite_remove, name='favorite_remove'),
]