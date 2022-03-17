from django.shortcuts import render
from django.urls import path

from . import views

urlpatterns = [
    path('auth/', render, kwargs={'template_name': 'auth.html'}, name='auth_page'),
    path('registration/', render, kwargs={'template_name': 'registration.html'}, name='registration_page'),
    path('profile/', render, kwargs={'template_name': 'lk.html'}, name='profile_page')
]
