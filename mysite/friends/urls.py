from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:id>/', views.profile, name='profile'),
    path('my_friends/', views.my_friends, name='my_friends'),
    path('messages/', views.messages, name='messages'),
    path('register/', views.register_user, name='register'),
]