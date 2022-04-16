from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=255, verbose_name='Логин', null=True,unique=True)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    second_name = models.CharField(max_length=255, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email')
    password = models.CharField(max_length=255, verbose_name='Пароль')
    time_registration = models.DateTimeField(auto_now_add=True, verbose_name='Время регистрации')
    
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class Post(models.Model):
    title = models.CharField(max_length=300, verbose_name="Текст")
    user = models.ForeignKey('User', related_name="posts", on_delete=models.CASCADE, verbose_name="Пользователь")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Пользовательский пост"
        verbose_name_plural = "Пользовательские посты"

class Follow(models.Model):
    user = models.ForeignKey("User", related_name="followers", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)
    following_user = models.ForeignKey("User", related_name="following", verbose_name="Подписчики", on_delete=models.CASCADE,null=True)
    time_following = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки",null=True)

    class Meta:
        verbose_name = 'Подписчики'
        verbose_name_plural = 'Подписчики'