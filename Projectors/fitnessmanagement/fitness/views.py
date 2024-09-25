from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from fitness.models import *
from .forms import LoginForm
from django.contrib.auth.models import Group
from .forms import LoginForm, EditProfileForm, RegistrationForm

# Index page
class IndexView(View):
    def get(self, request):
        return render(request, 'user/index.html')

#Login form
class LoginFormView(View):
    def get(self, request):
        form = LoginForm()
        context = {'form':form}
        return render(request, 'authen/login_form.html', context)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:  # Check if user is staff
                return redirect('manage')  # Redirect to management page
            else:
                messages.success(request, 'Login Success')
                return redirect('index')
        else:
            messages.error(request, 'There was an error. Please try again.')
            return redirect('login')

#Logout
class LogoutFormView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Logout Success')
        storage = messages.get_messages(request)
        storage.used = True  # clear the messages
        return redirect('login')

#Register form
class RegisterFormView(View):
    def get(self, request):
        form = RegistrationForm()
        context = {'form':form}
        return render(request, 'authen/register_form.html', context)

    def post(self, request):
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                role = form.cleaned_data['role']
                group_name = role.capitalize() 
                group, created = Group.objects.get_or_create(name=group_name)
                user.groups.add(group)
                login(request, user)
                return redirect('login')
        else:
            form = RegistrationForm()
        return render(request, 'authen/register_form.html', {'form': form})

#Membership page
class MembershipView(LoginRequiredMixin, View):
    def get(self, request):
        member = Membership.objects.all()
        context = {'member': member}
        return render(request, 'user/membership.html', context)

#Membership form
class MembershipFormView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user/membership_form.html')

#Fitnes class page
class FitnessClassView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user/fitness_class.html')
    
#Fitness class detail page
class FitnessClassDetailView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user/class_detail.html')

#Edit fitness class form
class EditFitnessClassView(LoginRequiredMixin, View):
    def get (self, request):
        return render(request, 'user/edit_class.html')

#Create fitness class form
class CreateFitnessClassView(LoginRequiredMixin, View):
    def get (self, request):
        return render(request, 'user/create_class.html')

#Userprofile page
class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, pk):
        return render(request, 'user/userprofile.html')

#Edit userprofile form
class EditProfileView(LoginRequiredMixin, View):
    def get(self, request, pk):
        form = EditProfileForm()
        return render(request, 'user/edit_profile.html', {'form': form})
    
    def post(self, request, pk):
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return render(request, 'user/userprofile.html', {'pk': pk})
        else:
            form = EditProfileForm(instance=request.user)
        return render(request, 'user/edit_profile.html', {'form': form})

# Change password form
class Change_PasswordView(LoginRequiredMixin, View):
    def get(self, request, pk):
        form = PasswordChangeForm(user=request.user)
        return render(request, 'user/change_password.html', {'form': form})

    def post(self, request, pk):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            print("save success")
            messages.success(request, 'Your password has been changed successfully.')
            return render(request, 'user/userprofile.html', {'pk':pk})
        else:
            print("unsave")
            return render(request, 'user/change_password.html', {'form': form})

# Admin page
class ManagementView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'admin/management.html')
    
# Manage user page
class ManageUserView(LoginRequiredMixin, View):
    def get(self, request):
        groups = Group.objects.all()
        user_list = User.objects.all().order_by('date_joined')
        return render(request, 'admin/manage_user.html', {'user_list': user_list, 'groups': groups})
    
    def post(self, request):
        selected_role = request.POST.get('role')
        groups = Group.objects.all()
        if selected_role:
            user_list = User.objects.filter(groups__name=selected_role).order_by('date_joined')
        else:
            user_list = User.objects.all().order_by('date_joined')
        count = User.objects.filter(groups__name=selected_role).count()
        return render(request, 'admin/manage_user.html', {'user_list': user_list, 'groups': groups, 'selected_role': selected_role, 'count': count})