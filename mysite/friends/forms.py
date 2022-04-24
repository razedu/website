from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from . import models


class RegisterUserForm(forms.ModelForm):
    password2 = forms.CharField(label="Повтор пароля")
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароль не совпадает')
        else:
            return cd

class LoginUserForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль')
