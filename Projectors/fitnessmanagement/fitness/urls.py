from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # Homepage
    path('login/', LoginFormView.as_view(), name='login'), # Login
    path('logout/', LogoutFormView.as_view(), name='logout'), # Logout
    path('register/', RegisterFormView.as_view(), name='register'), # Register
    path('userprofile/id:<int:pk>/', UserProfileView.as_view(), name='userprofile'), # User profile page
    path('edit_profile/id:<int:pk>/', EditProfileView.as_view(), name='edit_profile'), # Edit user profile page
    path('change_password/id:<int:pk>/', Change_PasswordView.as_view(), name='change_password'), # Change password page
    path('membership/', MembershipView.as_view(), name='membership'), # Membership page
    path('membership/membership_id/', MembershipFormView.as_view(), name='membership_form'),  # Membership form page
    path('class/', FitnessClassView.as_view(), name='class'), # Fitness class page
    path('class/create_class/', CreateFitnessClassView.as_view(), name='create-class'), # Create fitness class page
    path('class/id:<int:pk>/', FitnessClassDetailView.as_view(), name='class-detail'), # Fitness class detail page
    path('class/class_id/edit/', EditFitnessClassView.as_view(), name='edit-class'), # Edit fitness class page
    path('manage/', ManagementView.as_view(), name='manage'), # Admin
    path('manage/user/', ManageUserView.as_view(), name='manage-user'), # Manage user
    path('manage/user/delete/id:<int:pk>/', DeleteUserView.as_view(), name='delete-user'), # Delete user
    path('manage/membership/', ManageMembershipView.as_view(), name='manage-membership'), # Manage membership
]