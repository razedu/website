from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password

from .models import *
from . import forms
# Create your views here.
left_menu = [{'title':'Followers', 'url_name':'followers'},
{'title':'Posts', 'url_name':'messages'},
{'title':'Registration', 'url_name':'register'}
]

def home(request):
    user = User.objects.get(username=request.user.username)
    user_posts = user.following.user.posts.all()
    context = {
        'menu':left_menu,
        'user_posts':user_posts,
    }
    return render(request, 'friends/base.html', context=context)

def profile(request, id):
    user = User.objects.get(id = id)
    posts = user.posts.all()
    followers = user.followers.count()
    is_follow = False if user.followers.filter(following_user = request.user) else True
    context = {
        'user':user,
        'menu':left_menu,
        'posts':posts,
        'followers':followers,
        'is_follow':is_follow,
    }
    return render(request, 'friends/user.html', context=context)

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
                return redirect('profile', id=user.pk)
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
            login(request, user)
            return redirect('profile',id=user.pk)
    else:
        form = forms.RegisterUserForm()
    return render(request, 'friends/register.html', {'form':form})

def follow_user(request, user_name):
    user = User.objects.get(username = user_name)
    print(request.user.pk)
    follow = Follow(user=user, following_user=request.user)
    follow.save()
    return redirect('profile', id=user.pk)

def my_followers(request):
    user = User.objects.get(username=request.user.username)
    followers = user.followers.all()
    context = {
        'followers':followers,
        'menu':left_menu,
    }
    return render(request, 'friends/followers.html', context=context)

def my_friends(request):
    pass

def messages(request):
    pass