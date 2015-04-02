from django import forms
from django.contrib.auth.models import User
from user_profile.models import UserProperties


class LoginForm(forms.Form):
    login = forms.CharField(min_length=5, max_length=30)
    password = forms.CharField()



class RegistrationForm(forms.Form):
    login = forms.CharField(min_length=5, max_length=30)      # check if no doubles
    nickname = forms.CharField(min_length=5, max_length=20)
    password1 = forms.CharField()
    password2 = forms.CharField()
    avatar = forms.ImageField()



class SettingsFrom(forms.Form):
    nickname = forms.CharField(min_length=5, max_length=20)
    email = forms.EmailField()
    avatar = forms.ImageField()
