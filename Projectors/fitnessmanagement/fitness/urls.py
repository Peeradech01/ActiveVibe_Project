from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # Homepage
    path('login/', LoginFormView.as_view(), name='login'), # Login
    path('logout/', LogoutFormView.as_view(), name='logout'), # Logout
    path('register/', RegisterFormView.as_view(), name='register'), # Register
    path('userprofile/<int:pk>/', UserProfileView.as_view(), name='userprofile'), # User profile page
    path('edit_profile/<int:pk>/', EditProfileView.as_view(), name='edit_profile'), # Edit user profile page
    path('change_password/<int:pk>/', Change_PasswordView.as_view(), name='change_password'), # Change password page
    path('membership/', MembershipView.as_view(), name='membership'), # Membership page
    path('membership/<int:pk>/', MembershipFormView.as_view(), name='membership_form'),  # Membership form page
    path('class/', FitnessClassView.as_view(), name='class'), # Fitness class page
    path('class/create_class/', CreateFitnessClassView.as_view(), name='create-class'), # Create fitness class page
    path('class/<int:pk>/', FitnessClassDetailView.as_view(), name='class-detail'), # Fitness class detail page
    path('class/edit/<int:pk>/', EditFitnessClassView.as_view(), name='edit-class'), # Edit fitness class page
    path('class/delete/<int:pk>/', DeleteFitnessClassView.as_view(), name='delete-class'), # Edit fitness class page


    path('manage/', ManagementView.as_view(), name='manage'), # Admin
    path('manage/user/', ManageUserView.as_view(), name='manage-user'), # Manage user
    path('manage/user/delete/<int:pk>/', DeleteUserView.as_view(), name='delete-user'), # Delete user
    path('manage/membership/', ManageMembershipView.as_view(), name='manage-membership'), # Manage membership
    path('manage/create_membership/', CreateMembershipView.as_view(), name='create-membership'), # Manage create membership   
    path('manage/edit_membership/<int:pk>/', EditMembershipView.as_view(), name='edit-membership'), # Manage edit membership   
    path('manage/delete_membership/<int:pk>/', DeleteMembershipView.as_view(), name='delete-membership'), # Manage delete membership 
    path('manage/category/', ManageCategoryView.as_view(), name='manage-category'), # Manage Category   
    path('manage/create_category/', CreateCategoryView.as_view(), name='create-category'), # Manage create category   
    path('manage/edit_category/<int:pk>/', EditCategoryView.as_view(), name='edit-category'), # Manage edit category   
    path('manage/delete_category/<int:pk>/', DeleteCategoryView.as_view(), name='delete-category'), # Manage edit category  
    path('manage/class/', ManageClassView.as_view(), name='manage-class'), # Manage Class    
    path('manage/delete_class/<int:pk>/', DeleteClassView.as_view(), name='admin-delete-class'), # Manage edit category   

]