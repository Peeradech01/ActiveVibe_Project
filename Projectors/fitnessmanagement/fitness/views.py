from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import LoginForm

from .forms import LoginForm, RegisterForm, EditProfileForm


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

class LoginFormView(View):
    def get(self, request):
        form = LoginForm()
        context = {'form':form}
        return render(request, 'login_form.html', context)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # messages.success(request, 'You have been logged in successfully')
            return redirect('index')
        else:
            messages.error(request, 'There was an error. Please try again.')
            return redirect('login')
            
class LogoutFormView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Logout Success')
        storage = messages.get_messages(request)
        storage.used = True  # clear the messages
        return redirect('login')

class RegisterFormView(View):
    def get(self, request):
        form = RegisterForm()
        context = {'form':form}
        return render(request, 'register_form.html', context)

    def post(self, request):
        return redirect('login')  

class MembershipView(View):
    def get(self, request):
        return render(request, 'membership.html')
    
class MembershipFormView(View):
    def get(self, request):
        return render(request, 'membership_form.html')
    
class FitnessClassView(View):
    def get(self, request):
        return render(request, 'fitness_class.html')
    
class FitnessClassDetailView(View):
    def get(self, request):
        return render(request, 'class_detail.html')
    
class UserProfileView(View):
    def get(self, request):
        return render(request, 'userprofile.html')

class EditProfileView(View):
    def get(self, request):
        form = EditProfileForm()
        return render(request, 'edit_profile.html', {'form': form})

# ChangePasswordForm
class Change_PasswordView(View):
    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        return render(request, 'change_password.html', {'form': form})

    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            print("save success")
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('userprofile')
        else:
            print("unsave")
            # messages.error(request, 'Please correct the error below.')
            return render(request, 'change_password.html', {'form': form})
    