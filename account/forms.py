from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': "Username",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control", 'placeholder': "Password",
    }))
