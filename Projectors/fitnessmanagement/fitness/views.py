from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import LoginForm

from .forms import LoginForm, RegisterForm
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
            messages.success(request, 'You have been logged in successfully')
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
