from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:id>/', views.profile, name='profile'),
    path('my_friends/', views.my_friends, name='my_friends'),
    path('messages/', views.messages, name='messages'),
    path('all_users/', views.all_users, name='all_users'),
    path('news/', views.get_news, name='get_news'),
    path('register/', views.register_user, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('follow/<int:user_id>', views.follow_user, name='follow'),
    path('unfollow/<int:user_id>', views.unfollow_user, name='unfollow'),
    path('like/<int:post_id>', views.like_post, name='like_post'),
    path('unlike/<int:post_id>', views.like_delete, name='unlike_post'),
    path('followers/', views.my_followers, name='followers'),
    path('followed/', views.followed_user, name='followed'),
    path('post/delete_post/<int:post_id>', views.delete_post, name='delete_post'),
]