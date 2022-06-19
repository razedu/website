from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

from . import models


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    

class LoginUserForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль')

    def clean(self):
        cd = self.cleaned_data
        try:
            user = User.objects.get(username=cd['username'])
        except:
            raise forms.ValidationError('User does not exist')
        if user and check_password(cd['password'], user.password):
            return self.cleaned_data
        else:
            raise forms.ValidationError('Incorrect password')

class PostForm(forms.Form):
    text = forms.CharField(label='Text', max_length=500, widget=forms.Textarea(attrs={'class':'form-control', 'style':'height:100px'}))

class SearchUserForm(forms.Form):
    name = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={'class':'search-user-form form-control'}))

class ProfileEditForm(forms.Form):
    email = forms.EmailField(label='Email')
