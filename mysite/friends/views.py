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
left_menu = [{'title':'Followers', 'url_name':'my_friends'},
{'title':'Posts', 'url_name':'messages'},
{'title':'Registration', 'url_name':'register'}
]

def home(request):
    return render(request, 'friends/base.html')

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
    user.followers.add(request.user)
    return redirect('profile', id=user.pk)


def my_friends(request):
    pass

def messages(request):
    pass