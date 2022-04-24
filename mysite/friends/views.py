from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

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
    posts = Post.objects.filter(user_id = id)
    context = {
        'user':user,
        'menu':left_menu,
        'posts':posts,
    }
    return render(request, 'friends/user.html', context=context)

def user_login(request):
    if request.method == "POST":
        form = forms.LoginUserForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user = User.objects.get(username = username)
            if user:
                if user.password == password:
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
    if request.method == "POST":
        logout(request)
        return redirect('login')

# class RegisterUser(CreateView):
#     form_class = forms.RegisterUserForm
#     template_name = 'friends/register.html'
#     success_url = reverse_lazy('profile')
    
#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('profile')

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


def my_friends(request):
    pass

def messages(request):
    pass