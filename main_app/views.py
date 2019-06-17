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

def games_detail(request, game_id):
    game = Game.objects.get(id=game_id)
    return render(request, 'games/detail.html', {'game': game})

class CharacterCreate(CreateView):
    model = Character
    fields = ['name']

class GameCreate(CreateView):
    model = Game
    fields = '__all__'
