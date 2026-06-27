from django.contrib import admin
from .models import Category, Article, Comment, Favorite, Fact

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'created_at', 'views', 'is_published']
    list_filter = ['category', 'is_published']
    search_fields = ['title', 'content']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'created_at']

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'article']

@admin.register(Fact)
class FactAdmin(admin.ModelAdmin):
    list_display = ['text', 'is_active']
    list_filter = ['is_active']
    search_fields = ['text']