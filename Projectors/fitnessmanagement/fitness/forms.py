from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm



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



class EditProfileForm(UserChangeForm):
    password = None
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'edit-form', 'placeholder': 'Enter your username'}),
            'first_name': forms.TextInput(attrs={'class': 'edit-form', 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'edit-form', 'placeholder': 'Enter your last name'}),
            'email': forms.EmailInput(attrs={'class': 'edit-form', 'placeholder': 'Enter your email'}),
        }