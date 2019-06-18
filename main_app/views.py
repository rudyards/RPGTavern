
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .models import Profile, Character, Game, User

# Create your views here.
def home(request):
  return render(request, 'home.html')

@login_required
def profile(request):
    user = request.user
    games = Game.objects.all()
    characters = Character.objects.all()
    return render(request, 'profile.html',{'games': games, 'characters': characters})
  
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile_page')
        else:
            error_message = 'You Shall Not Pass! - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


# @login_required
# def profile(request):
#     return render(request, 'profile.html')


@login_required
def characters_detail(request, character_id):
    character = Character.objects.get(id=character_id)
    return render(request, 'characters/detail.html', {'character': character})
    

@login_required
def games_detail(request, game_id):
    game = Game.objects.get(id=game_id)
    return render(request, 'games/detail.html', {'game': game})


class CharacterCreate(LoginRequiredMixin, CreateView):
    model = Character
    fields = ['name']
    def form_valid(self, form):
        form.instance.player = self.request.user
        return super().form_valid(form)

class GameCreate(CreateView):
    model = Game
    fields = ['name', 'description']
    def form_valid(self, form):
        form.instance.admin = self.request.user 
        return super().form_valid(form)
