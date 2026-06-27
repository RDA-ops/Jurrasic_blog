from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileEditForm
from .models import Profile
from blog.models import Article, Favorite

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('blog:article_list')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Добро пожаловать!')
                return redirect('blog:article_list')
            else:
                messages.error(request, 'Неверный логин или пароль.')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('blog:article_list')

@login_required
def profile(request):
    profile = request.user.profile
    favorites = request.user.favorite_set.all()
    articles = request.user.article_set.all()
    return render(request, 'users/profile.html', {
        'profile': profile,
        'favorites': favorites,
        'articles': articles,
    })

@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлён.')
            return redirect('users:profile')
    else:
        form = ProfileEditForm(instance=profile)
    return render(request, 'users/profile_edit.html', {'form': form})
