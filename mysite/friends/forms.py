from django import forms

from . import models

class RegisterUserForm(forms.ModelForm):

    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'second_name', 'email', 'password']

class LoginUserForm():
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль')
