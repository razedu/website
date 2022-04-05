from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .models import *
from . import forms
# Create your views here.
left_menu = [{'title':'Друзья', 'url_name':'my_friends'},
{'title':'Сообщения', 'url_name':'messages'},
{'title':'Регистрация', 'url_name':'register'}
]

def profile(request, id):
    user = User.objects.get(id = id)
    context = {
        'user':user,
        'menu':left_menu,
    }
    return render(request, 'friends/user.html', context=context)

def user_login(request):
    pass

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
            return redirect('profile',id=1)
    else:
        form = forms.RegisterUserForm()
    return render(request, 'friends/register.html', {'form':form})


def my_friends(request):
    pass

def messages(request):
    pass