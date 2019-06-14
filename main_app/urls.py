from django.shortcuts import render, redirect
from django.urls import path, include
from . import views

urlpatterns = [
 path('profile/', views.profile, name='profile_page'),   
 path('accounts/', include('django.contrib.auth.urls')),
 
   
]