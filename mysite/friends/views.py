from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password
from django.db.models import Q

import requests
import os

from .models import *
from . import forms
# Create your views here.
left_menu = [{'title':'News', 'url_name':'get_news'},
{'title':'Followers', 'url_name':'followers'},
{'title':'Followed', 'url_name':'followed'},
{'title':'All users', 'url_name':'all_users'},
]


# Weather API
def get_weather(request):
    user_ip = request.META['REMOTE_ADDR']
    if user_ip == "127.0.0.1":
        user_city = "Moscow"
    else:
        user_city = requests.get(f"http://ip-api.com/json/{user_ip}").json()['city']
    params = {
        "units":"metric",
        "lang":"ru",
    }
    w_response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={user_city}&appid={os.getenv('WEATHER_API')}"
        , params=params).json()
    w_response['city'] = user_city
    return w_response

def get_nasa_data():
    response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={os.getenv('NASA_API')}")
    return response.json()['url']

@login_required(login_url='login/')
def home(request):
    my_user=request.user
    if request.method == "POST":
        form = forms.PostForm(request.POST)
        if form.is_valid():
            Post.objects.create(title=form.cleaned_data.get('text'), user=my_user)
            return HttpResponseRedirect('/')
    else:
        form = forms.PostForm()
    # user_posts = Post.objects.filter(Q(user__followers__following_user=my_user.pk)|Q(user_id=my_user.pk)).order_by('-time_create')
    users = Follow.objects.filter(following_user=my_user.pk).values('user')
    user_posts = Post.objects.filter(Q(user__in=users)|Q(user_id=my_user.pk)).order_by('-time_create')
    user_likes = [post.pk for post in Post.objects.filter(likes__user=request.user)]
    nasa = get_nasa_data()
    context = {
        'menu':left_menu,
        'user_posts':user_posts,
        'form':form,
        'user_likes':user_likes,
        'weather': get_weather(request),
    }
    return render(request, 'friends/base.html', context=context)

@login_required(login_url='login/')
def all_users(request):
    users = User.objects.all().exclude(pk=request.user.pk)
    user_followed = User.objects.filter(followers__following_user=request.user)
    context = {
        'menu':left_menu,
        'users':users,
        'user_followed':user_followed,
        'weather': get_weather(request),
    }
    return render(request,'friends/all_users.html', context=context)

@login_required(login_url='login/')
def profile(request, id):
    user = User.objects.get(id = id)
    posts = user.posts.all().order_by('-time_create')
    followers = user.followers.count()
    is_follow = False if not user.followers.filter(following_user = request.user) else True
    context = {
        'user':user,
        'menu':left_menu,
        'posts':posts,
        'followers':followers,
        'is_follow':is_follow,
        'weather': get_weather(request),
    }
    return render(request, 'friends/user.html', context=context)

@login_required(login_url='login/')
def get_news(request):
    api_key = os.getenv("NEWS_API")
    link = "https://newsapi.org/v2/everything"

    headers={
    "X-Api-Key":api_key,
    }

    params = {
        "sources":"RT",
    }

    response = requests.get(url=link, headers=headers, params=params)
    news = response.json()['articles']

    context = {
        'menu': left_menu,
        'news': news,
        'weather': get_weather(request),
    }

    return render(request, 'friends/news.html', context=context)

def user_login(request):
    if request.method == "POST":
        form = forms.LoginUserForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user = User.objects.get(username=username)
            if user:
                user_data = authenticate(
                    request,
                    username=username,
                    password=password)
                login(request, user_data)
                return redirect('home')
    else:
        form = forms.LoginUserForm()
    return render(request, 'friends/login.html', {'form':form})

def user_logout(request):
    logout(request)
    return redirect('home')


def register_user(request):
    if request.method == "POST":
        form = forms.RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = forms.RegisterUserForm()
    return render(request, 'friends/register.html', {'form':form})

@login_required(login_url='login/')
def follow_user(request, user_id):
    if request.method == 'POST':
        follow = Follow(user_id=user_id, following_user=request.user)
        follow.save()
        return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='login/')
def unfollow_user(request, user_id):
    if request.method == 'POST':
        follow = Follow.objects.get(user=user_id, following_user=request.user.pk)
        follow.delete()
        return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='login/')
def delete_follower(request, user_id):
    if request.method == 'POST':
        follow = Follow.objects.get(user=request.user.id, following_user=user_id)
        follow.delete()
        return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='login/')
def my_followers(request):
    followers = User.objects.filter(following__user=request.user.pk)
    context = {
        'followers':followers,
        'menu':left_menu,
        'weather': get_weather(request),
    }
    return render(request, 'friends/followers.html', context=context)

@login_required(login_url='login/')
def followed_user(request):
    followed = User.objects.filter(followers__following_user=request.user.pk)
    context = {
        'followed':followed,
        'menu':left_menu,
        'weather': get_weather(request),
    }
    return render(request, 'friends/followed.html', context=context)

@login_required(login_url='login/')
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('profile', id=request.user.pk)

@login_required(login_url='login/')
def like_post(request, post_id):
    if request.method == 'POST':
        like = Like(user=request.user, post_id=post_id)
        like.save()
        return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='login/')
def like_delete(request, post_id):
    if request.method == 'POST':
        like = Like.objects.get(post=post_id, user=request.user.pk)
        like.delete()
        return redirect(request.META['HTTP_REFERER'])

def my_friends(request):
    pass

def messages(request):
    pass