from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import *
from django.forms.widgets import *
from datetime import datetime, timedelta

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    
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

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 3:
            raise ValidationError('Username must be at least 3 characters long')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists() and email != self.instance.email:
            raise ValidationError('Email already exists')
        return email

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(label='Email')
    ROLE_CHOICES = [
        ('Customer', 'Customer'),
        ('Trainer', 'Trainer'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role']

class RegistrationMemberForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    phone = forms.CharField(max_length=10)
    start_date = forms.DateTimeField(widget=forms.DateInput(attrs={'type':'date'}))
    duration = forms.ChoiceField(choices=[
        ('1_month', '1 Month'),
        ('3_months', '3 Months'),
        ('6_months', '6 Months'),
        ('1_year', '1 Year')
    ])

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'start_date', 'duration']



class ClassForm(forms.ModelForm):
    categories = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class': 'cat'}))
    start_time = forms.DateTimeField(initial=datetime.now(), widget=DateTimeInput(format='%Y-%m-%d %H:%M', attrs={'type': 'datetime-local', 'class': 'input-detail'}))
    end_time = forms.DateTimeField(initial=datetime.now(), widget=DateTimeInput(format='%Y-%m-%d %H:%M', attrs={'type': 'datetime-local', 'class': 'input-detail'}))

    class Meta:
        model = FitnessClass
        fields = ('name', 'categories', 'description', 'start_time', "end_time", 'max_capacity')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-detail'}),
            'description': forms.Textarea(attrs={'class': 'input-detail', 'style': 'width:100%;'}),
            'max_capacity': forms.NumberInput(attrs={'class': 'input-detail'})
        }


class AdminMembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ('name', 'description', 'duration', 'price')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'width:100%;'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'})
        }


class AdminCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'bmi')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'bmi': forms.NumberInput(attrs={'class': 'form-control'})
        }