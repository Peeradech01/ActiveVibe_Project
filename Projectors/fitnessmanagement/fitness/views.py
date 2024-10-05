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
import random
from fitness.models import *
from .forms import LoginForm
from django.contrib.auth.models import Group
from .forms import LoginForm, EditProfileForm, RegistrationForm, ClassForm, AdminMembershipForm, AdminCategoryForm, UserForm, PersonalForm, ProfileImageForm

# Index page
class IndexView(View):
    def get(self, request):
        fitness_classes = FitnessClass.objects.all()
        if len(fitness_classes) >= 3:
            random_classes = random.sample(list(fitness_classes), 3)
        else:
            random_classes = list(fitness_classes)    
        context = {'random_classes': random_classes}
        return render(request, 'user/index.html', context)

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
            PersonalInfo.objects.create(
                customer=user,
            )

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
    def get(self, request, pk):
        membership = Membership.objects.get(pk=pk)
        if membership.duration >= 12:
            membership.duration_display = f"{membership.duration // 12} year"
        else:
            membership.duration_display = f"{membership.duration} month"
        form = UserForm()
        personal_form = PersonalForm()    
        context = {'form':form, 'personal_form':personal_form, 'pk':pk, 'membership':membership}
        print('this method get')
        return render(request, 'user/membership_form.html', context)
    
    def post(self, request, pk):
        form = UserForm(request.POST, instance=request.user)
        new_personal = False

        personal_form = PersonalForm(request.POST, instance=request.user.personalinfo)
        print('update customer')

        membership = Membership.objects.get(pk=pk)

        if form.is_valid() and personal_form.is_valid():
            user = form.save()

            personal_form.save()
            print('update_personal')

            # get membership
            
            # customer เคยลง membership อยู่แล้ว 
            try:
                # Check if CustomerMembership exists using get()
                customer_membership = CustomerMembership.objects.get(customer=user)
                print(f'customer : {customer_membership}')

                messages.error(request, "You already have a membership.", extra_tags='membership_registration')
                return redirect('membership_form', pk=pk) 
            
            # customer ยังไม่เคยลง membership
            except CustomerMembership.DoesNotExist:
                # Create new CustomerMembership 
                CustomerMembership.objects.create(
                    customer=user,
                    membership=membership
                )
                # messages.success(request, "Membership created successfully.")
                messages.success(request, "You registered membership successfully.", extra_tags='membership_registration')
                return redirect('membership')
        else:
            if membership.duration >= 12:
                membership.duration_display = f"{membership.duration // 12} year"
            else:
                membership.duration_display = f"{membership.duration} month"
            context = {'form': form, 'personal_form': personal_form, 'membership':membership, 'pk': pk}
            return render(request, 'user/membership_form.html', context)

# Fitness class page
class FitnessClassView(LoginRequiredMixin, View):
    def get(self, request):
        fit_class = FitnessClass.objects.all()
        categories = Category.objects.all()
        is_trainer = request.user.groups.filter(name='Trainer').exists()
        context = {'fit_class': fit_class, 'category_list': categories, 'is_trainer':is_trainer}
        return render(request, 'user/fitness_class.html', context)

    def post(self, request):
        fit_class = FitnessClass.objects.all()
        select_category = request.POST.get('category')
        search_query = request.POST.get('q')
        height_info = request.POST.get('height')
        weight_info = request.POST.get('weight')
        categories = Category.objects.all()
        if height_info and weight_info:
            bmi_info = float(weight_info) / (float(height_info) / 100) ** 2
            try:
                # update
                info_update = PersonalInfo.objects.get(customer=request.user.pk)
                info_update.weight = weight_info
                info_update.height = height_info
                info_update.bmi = bmi_info
                info_update.save()
            except:
                # create
                PersonalInfo.objects.create(
                    customer = request.user, 
                    height = height_info, 
                    weight = weight_info, bmi = bmi_info
                    )
            if select_category:
                category = Category.objects.get(name=select_category)
                if search_query:
                    fit_class = FitnessClass.objects.filter(categories__name=select_category, name__icontains=search_query, categories__bmi__lte=bmi_info)
                else:
                    fit_class = FitnessClass.objects.filter(categories__name=select_category, categories__bmi__lte=bmi_info)
            else:
                if search_query:
                    fit_class = FitnessClass.objects.filter(name__icontains=search_query, categories__bmi__lte=bmi_info)
                else:
                    fit_class = FitnessClass.objects.filter(categories__bmi__lte=bmi_info)
        elif select_category:
            if search_query:
                fit_class = FitnessClass.objects.filter(categories__name=select_category, name__icontains=search_query)
            else:
                fit_class = FitnessClass.objects.filter(categories__name=select_category)
        else:
            if search_query:
                fit_class = FitnessClass.objects.filter(name__icontains=search_query)
            else:
                fit_class = FitnessClass.objects.all()
        context = {'fit_class': fit_class, 'category_list': categories, 'select_category': select_category}
        return render(request, 'user/fitness_class.html', context)

#Fitness class detail page
class FitnessClassDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        fit_classdetail = FitnessClass.objects.get(pk=pk)
        is_trainer = request.user.groups.filter(name="Trainer")
        remaining = fit_classdetail.max_capacity - fit_classdetail.customer.count()
        context = {'fit_classdetail':fit_classdetail, 'is_trainer':is_trainer, 'remaining':remaining}
        return render(request, 'user/class_detail.html', context)
    
    def post(self, request, pk):
        fit_class = FitnessClass.objects.get(pk=pk)
        print(fit_class.customer.all())
        print(request.user)
        if request.user in fit_class.customer.all():
            messages.error(request, "You have already registered for this class.", extra_tags='class_registration')
            return redirect('class-detail', pk=pk)
        else:
            fit_class.customer.add(request.user)
            messages.success(request, "Registration FitnessClass successful.", extra_tags='class_registration_success')
        return redirect('class')

#Edit fitness class form
class EditFitnessClassView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'fitness.change_fitnessclass'
    def get(self, request, pk):
        fit_classdetail = FitnessClass.objects.get(pk=pk)
        if fit_classdetail.trainer == request.user:
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
class CreateFitnessClassView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'fitness.add_fitnessclass'
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
class DeleteFitnessClassView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'fitness.delete_fitnessclass'
    def get(self, request, pk):
        fit_classdetail = FitnessClass.objects.get(pk=pk)
        if fit_classdetail.trainer == request.user:
            fit_classdetail.delete()
            return redirect('class')
        if request.user.is_staff:
            return redirect('manage-class')

# UserProfile page
class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, pk):
        membership = CustomerMembership.objects.filter(customer=pk)
        customer_class = FitnessClass.objects.filter(customer=request.user)
        print(customer_class)
        context = {'membership': membership, 'customer_class': customer_class}
        return render(request, 'user/userprofile.html', context)

#Edit userprofile form
class EditProfileView(LoginRequiredMixin, View):
    def get(self, request, pk):
        form = EditProfileForm(instance=request.user)
        profile_form = ProfileImageForm()
        context = {'form':form, 'profile_form':profile_form}
        return render(request, 'user/edit_profile.html', context)
    
    def post(self, request, pk):
        personal_user = PersonalInfo.objects.get(customer=request.user.id) 

        # อัปเดตข้อมูลใน profile_form
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        profile_form = ProfileImageForm(request.POST, request.FILES, instance=personal_user)

        if form.is_valid() and profile_form.is_valid():
            form.save()  # บันทึกข้อมูลผู้ใช้
            profile_form.save()  # บันทึกข้อมูล PersonalInfo
            messages.success(request, 'Profile Updated Successfully', extra_tags="updateprofile")
            return render(request, 'user/userprofile.html', {'pk': pk})
        else:
            context = {'form': form, 'profile_form': profile_form}
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
            messages.success(request, 'Your password has been changed successfully.', extra_tags="changepassword")
            return render(request, 'user/userprofile.html', {'pk':pk})
        else:
            print("unsave")
            context = {'form': form}
            return render(request, 'user/change_password.html', context)

# Admin page
class ManagementView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_staff:
            category = Category.objects.all()
            user = User.objects.all()
            membership = Membership.objects.all()
            classes = FitnessClass.objects.all()
            context = {'category': category, 'user': user, 'membership': membership, 'classes': classes}
            return render(request, 'admin/management.html', context)
        else:
            return ForbiddenView.as_view()(request)
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
    def get(self, request, pk):
        membership = Membership.objects.get(pk=pk)
        form = AdminMembershipForm(instance=membership)
        context = {'form':form, 'membership':membership}
        return render(request, 'admin/edit_membership.html', context)
    
    def post(self, request, pk):
        membership = Membership.objects.get(pk=pk)
        form = AdminMembershipForm(request.POST, instance=membership)
        if form.is_valid():
            form.save()
            return redirect('manage-membership')
        else:
            context = {'form':form, 'membership':membership}
            return render(request, 'admin/edit_membership.html', context)

# Manage delete membership
class DeleteMembershipView(LoginRequiredMixin, View):
    def get(self, request, pk):
        membership = Membership.objects.get(pk=pk)
        membership.delete()
        return redirect('manage-membership')

# Manage create category
class CreateCategoryView(LoginRequiredMixin, View):
    def get(self, request):
        form = AdminCategoryForm()
        context = {'form':form}
        return render(request, 'admin/create_category.html', context)
    def post(self, request):
        form = AdminCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage-category')
        else:
            context = {'form':form}
            return render(request, 'admin/create_category.html', context)

# Manage edit category
class EditCategoryView(LoginRequiredMixin, View):
    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        form = AdminCategoryForm(instance=category)
        context = {'form':form, 'category':category}
        return render(request, 'admin/edit_category.html', context)
    def post(self, request, pk):
        category = Category.objects.get(pk=pk)
        form = AdminCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('manage-category')
        else:
            context = {'form':form, 'category':category}
            return render(request, 'admin/edit_category.html', context)

# Manage Delete category
class DeleteCategoryView(LoginRequiredMixin, View):
    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.delete()
        return redirect('manage-category')
    
# Manage Deletee class
class DeleteClassView(LoginRequiredMixin, View):
    def get(self, request, pk):
        class_del = FitnessClass.objects.get(pk=pk)
        class_del.delete()
        return redirect('manage-class')


class ForbiddenView(View):
    def get(self, request):
        return render(request, '403.html')