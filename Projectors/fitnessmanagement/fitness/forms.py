from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    


class RegisterForm(UserCreationForm):
    ROLE_CHOICES = [
        ('Customer', 'Customer'),
        ('Trainer', 'Trainer'),
    ]
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, label='Role')
    
    class Meta:
        model=User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2'] 