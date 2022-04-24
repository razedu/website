from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=300, verbose_name="Текст")
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE, verbose_name="Пользователь")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Пользовательский пост"
        verbose_name_plural = "Пользовательские посты"

class Follow(models.Model):
    user = models.ForeignKey(User, related_name="followers", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)
    following_user = models.ForeignKey(User, related_name="following", verbose_name="Подписчики", on_delete=models.CASCADE,null=True)
    time_following = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки",null=True)

    class Meta:
        verbose_name = 'Подписчики'
        verbose_name_plural = 'Подписчики'