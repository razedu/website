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

from .models import *
from . import forms
# Create your views here.
left_menu = [{'title':'Followers', 'url_name':'followers'},
{'title':'Followed', 'url_name':'followed'},
{'title':'Posts', 'url_name':'messages'},
{'title':'All users', 'url_name':'all_users'},
]

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
    user_likes = Post.objects.filter(likes__user=request.user)
    print(user_likes)
    context = {
        'menu':left_menu,
        'user_posts':user_posts,
        'form':form,
        'user_likes':user_likes,
    }
    return render(request, 'friends/base.html', context=context)

def all_users(request):
    users = User.objects.all().exclude(pk=request.user.pk)
    user_followed = User.objects.filter(followers__following_user=request.user)
    context = {
        'menu':left_menu,
        'users':users,
        'user_followed':user_followed,
    }
    return render(request,'friends/all_users.html', context=context)

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
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('profile',id=user.pk)
    else:
        form = forms.RegisterUserForm()
    return render(request, 'friends/register.html', {'form':form})

def follow_user(request, user_id):
    user = User.objects.get(pk = user_id)
    follow = Follow(user=user, following_user=request.user)
    follow.save()
    return redirect('profile', id=user_id)

def unfollow_user(request, user_id):
    follow = Follow.objects.get(user=user_id, following_user=request.user.pk)
    follow.delete()
    return redirect('profile', id=user_id)

def my_followers(request):
    followers = User.objects.filter(following__user=request.user.pk)
    context = {
        'followers':followers,
        'menu':left_menu,
    }
    return render(request, 'friends/followers.html', context=context)

def followed_user(request):
    followed = User.objects.filter(followers__following_user=request.user.pk)
    context = {
        'followed':followed,
        'menu':left_menu,
    }
    return render(request, 'friends/followed.html', context=context)

def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('profile', id=request.user.pk)

def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    like = Like(user=request.user, post=post)
    like.save()
    return redirect('home')

def like_delete(request, post_id):
    like = Like.objects.get(post=post_id, user=request.user.pk)
    like.delete()
    return redirect('home')

def my_friends(request):
    pass

def messages(request):
    pass