from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.decorators.cache import cache_page
from .models import Article, Category, Comment, Favorite, Fact  # Fact должен быть!
from .forms import ArticleForm, CommentForm
from .filters import ArticleFilter
from .tasks import send_new_article_notification
import logging
import random  # добавьте random, если его нет
import requests

DINO_FACTS = [
    'Тираннозавр мог съесть до 200 кг мяса за один раз.',
    'Стегозавр имел мозг размером с грецкий орех.',
    'Велоцирапторы были покрыты перьями.',
    'Трицератопс мог весить до 12 тонн.',
    'Диплодок достигал длины 27 метров.',
    'Птеранодон размах крыльев — 7 метров.',
    'Анкилозавр имел хвост-булаву.',
    'Брахиозавр достигал высоты 13 метров.',
    'Паразауролоф издавал громкие звуки через свой гребень.',
]

def article_list(request):
    # Получаем все опубликованные статьи
    articles = Article.objects.filter(is_published=True)
    
    # Фильтрация по категории
    category_id = request.GET.get('category')
    if category_id:
        articles = articles.filter(category_id=category_id)
    
    # Получаем все категории для меню
    categories = Category.objects.all()
    
    # Случайный факт из базы данных
    facts = Fact.objects.filter(is_active=True)
    if facts.exists():
        dino_fact = random.choice(facts).text
    else:
        dino_fact = 'Динозавры — удивительные существа.'
    
    context = {
        'articles': articles,
        'categories': categories,
        'dino_fact': dino_fact,
    }
    return render(request, 'blog/article_list.html', context)

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.views += 1
    article.save()

    comments = article.comments.all()
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.article = article
            comment.save()
            messages.success(request, 'Комментарий добавлен.')
            return redirect('blog:article_detail', pk=article.pk)
    else:
        form = CommentForm()

    context = {
        'article': article,
        'comments': comments,
        'form': form,
    }
    return render(request, 'blog/article_detail.html', context)

@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, 'Статья создана!')
            return redirect('blog:article_detail', pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'blog/article_create.html', {'form': form})

@login_required
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user != article.author and not request.user.is_superuser:
        messages.error(request, 'Вы не можете редактировать эту статью.')
        return redirect('blog:article_detail', pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статья обновлена.')
            return redirect('blog:article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'blog/article_edit.html', {'form': form, 'article': article})

@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user != article.author and not request.user.is_superuser:
        messages.error(request, 'Вы не можете удалить эту статью.')
        return redirect('blog:article_detail', pk=pk)
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Статья удалена.')
        return redirect('blog:article_list')
    return render(request, 'blog/article_delete.html', {'article': article})

@login_required
def favorite_add(request, pk):
    article = get_object_or_404(Article, pk=pk)
    Favorite.objects.get_or_create(user=request.user, article=article)
    messages.success(request, 'Статья добавлена в избранное.')
    return redirect('blog:article_detail', pk=pk)

@login_required
def favorite_remove(request, pk):
    article = get_object_or_404(Article, pk=pk)
    Favorite.objects.filter(user=request.user, article=article).delete()
    messages.success(request, 'Статья удалена из избранного.')
    return redirect('blog:article_detail', pk=pk)

def custom_404(request, exception):
    return render(request, 'blog/404.html', status=404)

def custom_500(request):
    return render(request, 'blog/500.html', status=500)
