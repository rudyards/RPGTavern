from django.urls import path, include
from . import views

urlpatterns = [
 path('profile/', views.profile, name='profile_page'),   
 path('accounts/', include('django.contrib.auth.urls')),
 path('accounts/signup', views.signup, name='signup'),
   
]