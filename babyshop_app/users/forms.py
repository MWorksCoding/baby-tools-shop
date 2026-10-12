from dataclasses import fields
from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class RegisterForm(UserCreationForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'First name'
    }))
    last_name=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Last name'
    }))
    username=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Username'
    }))
    email=forms.CharField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Email'
    }))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Password'
    }))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Repeat password'
    }))
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password1','password2']




class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Username'
    }))
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Password'
    }))


