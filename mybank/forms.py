from django.forms import ModelForm
from .models import CustomUser,Account
from django import forms



class UserRegistrationForm(ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=CustomUser
        fields=["username","email","password","age","phone"]


class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()


class AccountCreationForm(ModelForm):
    account_number = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model=Account
        fields=["account_number","balance","account_type","user","active_status"]

