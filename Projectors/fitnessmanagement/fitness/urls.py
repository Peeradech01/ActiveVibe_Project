from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('register/', RegisterFormView.as_view(), name='register'),
    path('membership/', MembershipView.as_view(), name='membership'),
    path('membership/membership_id', MembershipFormView.as_view(), name='membership_form'),
]