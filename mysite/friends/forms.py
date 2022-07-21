from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password, make_password

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

class EmailEditForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100,widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter new Email'}))

class PasswordEditForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
            self.user = user
            super().__init__(*args, **kwargs)
    
    password1 = forms.CharField(label='Previous Password', max_length=16, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Prev password'}))
    password2 = forms.CharField(label='Password', max_length=16, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'New password'}))
    password3 = forms.CharField(label='Repeat Password', max_length=16, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'New password'}))

    def clean(self):
        cd = self.cleaned_data
        print(self.user)
        user = User.objects.get(id=self.user)
        if check_password(cd['password1'], user.password):
            if cd['password2'] == cd['password3']:
                cd['password2'] = make_password(cd['password2'])
                return cd
            else:
                print('New password does not match')
                raise forms.ValidationError('New password does not match') 
        else:
            print('Previous password error')
            raise forms.ValidationError('Previous password error')
