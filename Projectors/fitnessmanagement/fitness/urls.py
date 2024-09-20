from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutFormView.as_view(), name='logout'),
    path('register/', RegisterFormView.as_view(), name='register'),
    path('userprofile/', UserProfileView.as_view(), name='userprofile'),
    path('membership/', MembershipView.as_view(), name='membership'),
    path('membership/membership_id', MembershipFormView.as_view(), name='membership_form'),
    path('class/', FitnessClassView.as_view(), name='class'),
    path('class/class_id', FitnessClassDetailView.as_view(), name='class-detail'),
]