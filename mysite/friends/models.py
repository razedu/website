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

    def __str__(self) -> str:
        return self.first_name + self.second_name

