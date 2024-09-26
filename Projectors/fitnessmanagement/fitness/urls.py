from django.urls import path
from .views import *

urlpatterns = [
    # Homepage
    path('', IndexView.as_view(), name='index'),
    
    # Login 
    path('login/', LoginFormView.as_view(), name='login'),
    
    # Logout 
    path('logout/', LogoutFormView.as_view(), name='logout'),
    
    # Register
    path('register/', RegisterFormView.as_view(), name='register'),
    
    # User profile page
    path('userprofile/id:<int:pk>/', UserProfileView.as_view(), name='userprofile'),
    
    # Edit user profile page
    path('edit_profile/id:<int:pk>/', EditProfileView.as_view(), name='edit_profile'),
    
    # Change password page
    path('change_password/id:<int:pk>/', Change_PasswordView.as_view(), name='change_password'),
    
    # Membership page
    path('membership/', MembershipView.as_view(), name='membership'),
    
    # Membership form page
    path('membership/membership_id/', MembershipFormView.as_view(), name='membership_form'),
    
    # Fitness class page
    path('class/', FitnessClassView.as_view(), name='class'),
    
    # Create fitness class page
    path('class/create_class/', CreateFitnessClassView.as_view(), name='create-class'),
    
    # Fitness class detail page
    path('class/class_id/', FitnessClassDetailView.as_view(), name='class-detail'),
    
    # Edit fitness class page
    path('class/class_id/edit/', EditFitnessClassView.as_view(), name='edit-class'),

    # Admin
    path('manage/', ManagementView.as_view(), name='manage'),

    # Manage user
    path('manage/user/', ManageUserView.as_view(), name='manage-user'),

    # Delete user
    path('manage/user/delete/id:<int:pk>/', DeleteUserView.as_view(), name='delete-user'),

    # Manage membership
    path('manage/membership/', ManageMembershipView.as_view(), name='manage-membership'),
]