from django.shortcuts import render
from django.contrib.auth import login
from django.views.generic.edit import CreateView
from .models import Profile, Character, Game


# Create your views here.
def home(request):
  return render(request, 'home.html')

def profile(request):
    return render(request, 'profile.html')

def characters_detail(request, character_id):
    character = Character.objects.get(id=character_id)
    return render(request, 'characters/detail.html', {'character': character})

class CharacterCreate(CreateView):
    model = Character
    fields = ['name']

class GameCreate(CreateView):
    model = Game
    fields = '__all__'