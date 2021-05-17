from django.forms import ModelForm
from .models import CustomUser
from django import forms



class UserRegistrationForm(ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=CustomUser
        fields=["username","email","password","age","phone"]


class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()