from django.shortcuts import render
from .models import Profile
from django.contrib.auth import login


# Create your views here.
def home(request):
  return render(request, 'home.html')

def profile(request):
    return render(request, 'profile.html')