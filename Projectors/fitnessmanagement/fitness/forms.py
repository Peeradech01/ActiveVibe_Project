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

# Admin create_edit membership
class AdminMembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ['name', 'description', 'duration', 'price']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'font-size: 1.5rem;'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'width:100%; font-size: 1.5rem'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'style': 'font-size: 1.5rem;'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'style': 'font-size: 1.5rem;'})
        }
    def clean_name(self):
        name_form = self.cleaned_data['name']
        member_id = self.instance.pk
        if Membership.objects.filter(name=name_form).exclude(pk=member_id):
            raise forms.ValidationError("Name does exist already")
        return name_form
    def clean_duration(self):
        duration = self.cleaned_data["duration"]
        if duration <= 0:
            raise forms.ValidationError("Duration must be positive integer")
        return duration
    def clean_price(self):
        price = self.cleaned_data["price"]
        if price <= 0:
            raise forms.ValidationError("Price must be positive integer")
        return price


# Admin create_edit category
class AdminCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'bmi']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'font-size: 1.5rem;'}),
            'bmi': forms.NumberInput(attrs={'class': 'form-control', 'style': 'font-size: 1.5rem;'})
        }

    def clean_name(self):
        name_form = self.cleaned_data['name']
        cat_id = self.instance.pk
        if Category.objects.filter(name=name_form).exclude(pk=cat_id):
            raise forms.ValidationError("Name does exist already")
        return name_form


    def clean_bmi(self):
        bmi = self.cleaned_data['bmi']
        if bmi <= 0:
            raise forms.ValidationError("BMI must be positive integer")
        return bmi


# model auth_user 
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email'] 

# model PersonalInfo
class PersonalForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = ['phone']
        