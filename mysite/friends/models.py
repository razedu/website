from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    avatar = models.FileField(default='avatar.png', upload_to='avatars/', verbose_name='Аватар')

    def __str__(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=300, verbose_name="Текст")
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE, verbose_name="Пользователь")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "User post"
        verbose_name_plural = "User posts"

class Follow(models.Model):
    user = models.ForeignKey(User, related_name="followers", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)
    following_user = models.ForeignKey(User, related_name="following", verbose_name="Подписчики", on_delete=models.CASCADE,null=True)
    time_following = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки",null=True)

    class Meta:
        verbose_name = 'Followers'
        verbose_name_plural = 'Followers'
        constraints = [
            models.UniqueConstraint(fields=['user', 'following_user'], name='user_unique')
        ]

class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', verbose_name='user_likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', verbose_name='liked_post', on_delete=models.CASCADE)
    time_like = models.DateTimeField(auto_now_add=True, verbose_name='liked_time')

    class Meta:
        verbose_name = 'Like'
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='like_unique')
        ]
        