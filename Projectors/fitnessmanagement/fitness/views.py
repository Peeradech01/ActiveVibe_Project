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
from .forms import LoginForm, EditProfileForm, RegistrationForm, ClassForm, RegistrationMemberForm, AdminMembershipForm

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
        context = {'form': form}
        return render(request, 'authen/register_form.html', context)

    def post(self, request):
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
            context = {'form': form}
            return render(request, 'authen/register_form.html', context)
#Membership page
class MembershipView(LoginRequiredMixin, View):
    def get(self, request):
        member = Membership.objects.all()
        context = {'member':member}
        return render(request, 'user/membership.html', context)

#Membership form
class MembershipFormView(LoginRequiredMixin, View):
    def get(self, request):
        form = RegistrationMemberForm()
        context = {'form':form}
        print('this method get')
        return render(request, 'user/membership_form.html', context)
    def post(self, request):
        print("this method post")
        form = RegistrationMemberForm(request.POST)
        user = form.save()
        print(user) 
        return render(request, 'user/membership_form.html')


#Fitnes class page
class FitnessClassView(LoginRequiredMixin, View):
    def get(self, request):
        fit_class = FitnessClass.objects.all()
        context = {'fit_class':fit_class}
        return render(request, 'user/fitness_class.html', context)


#Fitness class detail page
class FitnessClassDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        fit_classdetail = FitnessClass.objects.get(pk=pk)
        trainer_name = User.objects.get(pk=fit_classdetail.trainer_id)
        category_name = Category.objects.get(pk=fit_classdetail.categories_id)
        context = {'fit_classdetail':fit_classdetail, 'trainer': trainer_name, 'category': category_name}
        return render(request, 'user/class_detail.html', context)

#Edit fitness class form
class EditFitnessClassView(LoginRequiredMixin, View):
    def get(self, request, pk):
        fit_classdetail = FitnessClass.objects.get(pk=pk)
        form = ClassForm(instance=fit_classdetail)
        context = {'fit_classdetail':fit_classdetail,'form': form}
        return render(request, 'user/edit_class.html', context)
    
    def post(self, request, pk):
        form = ClassForm(request.POST, instance=FitnessClass.objects.get(pk=pk))
        if form.is_valid:
            form.save()
            return redirect('class-detail', pk=pk)
        else:
            context = {'form': form}
            return render(request, 'user/fitness_class.html', context)

#Create fitness class form
class CreateFitnessClassView(LoginRequiredMixin, View):
    def get(self, request):
        form = ClassForm()
        context = {'form': form}
        return render(request, 'user/create_class.html', context)

    def post(self, request):
        form = ClassForm(request.POST)
        if form.is_valid():
            trainer = request.user.pk
            form.instance.trainer_id = trainer
            form.save()
            return redirect('class')
        else:
            context = {'form': form}
            return render(request, 'user/create_class.html', context)
        
#Delete fitnes sclass
class DeleteFitnessClassView(LoginRequiredMixin, View):
    def get(self, request, pk):
        fit_classdetail = FitnessClass.objects.get(pk=pk)
        fit_classdetail.delete()
        return redirect('class')

#Userprofile page
class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, pk):
        return render(request, 'user/userprofile.html')

#Edit userprofile form
class EditProfileView(LoginRequiredMixin, View):
    def get(self, request, pk):
        form = EditProfileForm()
        context = {'form':form}
        return render(request, 'user/edit_profile.html', context)
    
    def post(self, request, pk):
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return render(request, 'user/userprofile.html', {'pk': pk})
        else:
            form = EditProfileForm(instance=request.user)
            context = {'form': form}
        return render(request, 'user/edit_profile.html', context)

# Change password form
class Change_PasswordView(LoginRequiredMixin, View):
    def get(self, request, pk):
        form = PasswordChangeForm(user=request.user)
        context = {'form': form}
        return render(request, 'user/change_password.html', context)

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
            context = {'form': form}
            return render(request, 'user/change_password.html', context)

# Admin page
class ManagementView(LoginRequiredMixin, View):
    def get(self, request):
        category = Category.objects.all()
        user = User.objects.all()
        membership = Membership.objects.all()
        classes = FitnessClass.objects.all()
        context = {'category': category, 'user': user, 'membership': membership, 'classes': classes}
        return render(request, 'admin/management.html', context)
    
# Manage user page
class ManageUserView(LoginRequiredMixin, View):
    def get(self, request):
        groups = Group.objects.all()
        user_list = User.objects.all().order_by('date_joined')
        context = {'user_list': user_list, 'groups': groups}
        return render(request, 'admin/manage_user.html', context)
    
    def post(self, request):
        selected_role = request.POST.get('role')
        groups = Group.objects.all()
        if selected_role:
            user_list = User.objects.filter(groups__name=selected_role).order_by('date_joined')
        else:
            user_list = User.objects.all().order_by('date_joined')
        count = User.objects.filter(groups__name=selected_role).count()
        context = {'user_list': user_list, 'groups': groups, 'selected_role': selected_role, 'count': count}
        return render(request, 'admin/manage_user.html', context)

# Delet user 
class DeleteUserView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        print("success")
        return redirect('manage-user')
    
# Manage membership page
class ManageMembershipView(LoginRequiredMixin, View):
    def get(self, request):
        membership_list = Membership.objects.all()
        for membership in membership_list:
            if membership.duration >= 12:
                membership.duration_display = f"{membership.duration // 12} year"
            else:
                membership.duration_display = f"{membership.duration} month"
        context = {'membership_list': membership_list}
        return render(request, 'admin/manage_membership.html', context)
    
# Manage category page
class ManageCategoryView(LoginRequiredMixin, View):
    def get(self, request):
        category_list = Category.objects.all()
        context = {'category_list':category_list}
        return render(request, 'admin/manage_category.html', context)

# Manage class page
class ManageClassView(LoginRequiredMixin, View):
    def get(self, request):
        class_list = FitnessClass.objects.all()
        context = {'class_list':class_list}
        return render(request, 'admin/manage_class.html', context)
    
# Manage create membership
class CreateMembershipView(LoginRequiredMixin, View):
    def get(self, request):
        form = AdminMembershipForm()
        context = {'form':form}
        return render(request, 'admin/create_membership.html', context)
    def post(self, request):
        form = AdminMembershipForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage-membership')
        else:
            context = {'form': form}
            return render(request, 'admin/create_membership.html', context)


# Manage edit membership
class EditMembershipView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'admin/edit_membership.html')

# Manage create category
class CreateCategoryView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'admin/create_category.html')

# Manage edit category
class EditCategoryView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'admin/edit_category.html')

