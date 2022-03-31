from django.shortcuts import render

from .models import *
# Create your views here.

def user(request, id):
    user = User.objects.get(id = id)
    context = {
        'user':user,
        'menu':'dsadsadasd'
    }
    return render(request, 'friends/user.html', context=context)