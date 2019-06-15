from django.shortcuts import render
from django.contrib.auth import login
from django.views.generic.edit import CreateView
from .models import Profile, Character


# Create your views here.
def home(request):
  return render(request, 'home.html')

def profile(request):
    return render(request, 'profile.html')

class CharacterCreate(CreateView):
    model = Character
    fields = ['name']