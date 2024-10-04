from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.core.validators import RegexValidator
from .models import *
from django.forms.widgets import *
from datetime import datetime, timedelta
from django.utils import timezone

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    
# upload profile image
class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = ['profile_image']

        widgets = {
            'profile_image': forms.FileInput(attrs={'class': 'edit-form'}),
        }

# edit profile
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

# register
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


# class
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
    def clean_name(self):
        name_form = self.cleaned_data['name']
        if FitnessClass.objects.filter(name=name_form).exists() and name_form != self.instance.name:
            raise forms.ValidationError("Name does exist already")
        return name_form
    def clean_max_capacity(self):
        max_capacity = self.cleaned_data["max_capacity"]
        if max_capacity <= 0:
            raise forms.ValidationError("Max capacity must be positive integer")
        return max_capacity
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        now = timezone.now()
        if start_time and start_time < now:
            self.add_error('start_time', 'Start time cannot be in the past.')
        if end_time and end_time <= start_time:
            self.add_error('end_time', 'End time must be after the start time.')
        return cleaned_data





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
        if Membership.objects.filter(name=name_form).exists() and name_form != self.instance.name:
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
        if Category.objects.filter(name=name_form).exists() and name_form != self.instance.name:
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
    
    def clean_first_name(self):
        first_name_form = self.cleaned_data['first_name']
        if first_name_form != self.instance.first_name:
            raise forms.ValidationError("First name not matched")
        return first_name_form
    def clean_last_name(self):
        last_name_form = self.cleaned_data['last_name']
        if last_name_form != self.instance.last_name:
            raise forms.ValidationError("Last name not matched")
        return last_name_form
    

# model PersonalInfo
class PersonalForm(forms.ModelForm):
    phone_validator = RegexValidator(
        regex=r'^(0)[0-9]{9}$',
        message="Phone number must be in format '0xxxxxxxxx'"
    )

    phone = forms.CharField(validators=[phone_validator])

    class Meta:
        model = PersonalInfo
        fields = ['phone']
