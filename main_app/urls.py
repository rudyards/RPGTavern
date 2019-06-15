from django.shortcuts import render, redirect
from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile_page'),
]