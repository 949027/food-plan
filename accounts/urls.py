from django.shortcuts import render
from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('registration/', views.UserCreateView.as_view(), name='registration'),
    path('profile/', views.user_profile, name='profile')
]
