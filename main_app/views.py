
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.views.generic.edit import CreateView
from .models import Profile, Meeting, Character, Game, Game_photo, Character_photo, Character_sheet_photo, Comment, Profile_photo
from .forms import MeetingForm
from .forms import CommentForm

import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'taverntalk'
# Create your views here.
def home(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'profile.html')
    else:
        return render(request, 'home.html')

@login_required
def profile(request):
    user = request.user
    gmgames = Game.objects.filter(admin=user.id)
    characters = Character.objects.filter(player=user.id)
    playergames = []
    for character in characters:
        if character.game:
            playergames.append(Game.objects.filter(id=character.game.id))
    if playergames:
        playergames = playergames[0]
    meetings = []
    for game in gmgames:
        sessions = Meeting.objects.filter(game=game.id)
        if sessions:
            for session in sessions:
                meetings.append([game, session])
    for game in playergames:
        sessions = Meeting.objects.filter(game=game.id)
        if sessions:
            for session in sessions:
                meetings.append([game, session])
    return render(request, 'profile.html',{'gmgames': gmgames, 'characters': characters, 'meetings': meetings, 'playergames': playergames})
  

def add_profile_photo(request, profile_id):
    profile_photo = Profile_photo.objects.all()
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Profile_photo(url=url, profile=profile_id)
            print('photo assining to model')
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('profile_page')


def add_character_photo(request, character_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Character_photo(url=url, character_id=character_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('characters_detail', character_id=character_id)

def add_character_sheet_photo(request, character_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Character_sheet_photo(url=url, character_id=character_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('characters_detail', character_id=character_id)


def add_game_photo(request, game_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Game_photo(url=url, game_id=game_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('games_detail', game_id=game_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile(user = user)
            profile.save()
            login(request, user)
            return redirect('profile_page')
        else:
            error_message = 'You Shall Not Pass! - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


@login_required
def characters_detail(request, character_id):
    character = Character.objects.get(id=character_id)
    character_photo = Character_photo.objects.filter(character=character.id)
    character_sheet_photo = Character_sheet_photo.objects.filter(character=character.id)
    return render(request, 'characters/detail.html', {'character': character, 'character_photo': character_photo, 'character_sheet_photo': character_sheet_photo})
    

@login_required
def games_detail(request, game_id):
    game = Game.objects.get(id=game_id)
    game_photo = Game_photo.objects.filter(game=game.id)
    comment = Comment.objects.filter(game=game.id)
    comment_form = CommentForm()
    meetings = Meeting.objects.filter(game=game.id)
    meeting_form = MeetingForm()
    characters = Character.objects.filter(game=game_id)
    return render(request, 'games/detail.html', {'game': game, 'game_photo': game_photo, 'meeting_form': meeting_form, 'meetings': meetings, 'comment_form': comment_form, 'comment':comment, 'characters': characters})


def add_meeting(request, game_id):
    form = MeetingForm(request.POST)
    if form.is_valid():
        new_meeting = form.save(commit=False)
        new_meeting.game_id = game_id
        new_meeting.save()
    return redirect('games_detail', game_id=game_id)

def add_comment(request, game_id):
    form = CommentForm(request.POST)
    user = request.user
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.game_id = game_id
        new_comment.user = user
        new_comment.save()
    return redirect('games_detail', game_id=game_id)

@login_required
def games_join(request, game_id):
    user = request.user
    games_in = []
    dm_games = Game.objects.filter(admin=user.id)
    characters =  Character.objects.filter(player=user.id)
    for game in dm_games:
        games_in.append(game)
    for character in characters:
        if character.game:
            game_search = Game.objects.filter(id=character.game.id)
            games_in.append(game_search[0])
    print(games_in)
    for game in games_in:
        if (game.id == game_id):
            #You're already in this game
            return redirect('home')

    characters =  Character.objects.filter(player=user.id).filter(game=None)
    return render(request, 'games/join.html', {'characters': characters, 'game_id': game_id})
            
@login_required
def games_join_yes(request, game_id):
    user = request.user
    game = Game.objects.filter(id=game_id)[0]
    character = Character.objects.filter(player=user.id).filter(name=request.POST.get('character'))
    character = character[0]
    character.game = game
    print(character.game)
    character.save()
    return redirect('games_detail', game_id=game_id)

def games_kick(request, game_id, character_id):
    character = Character.objects.filter(id=character_id)
    character = character[0]
    character.game = None
    character.save()
    return redirect('games_detail', game_id=game_id)    
    

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

class CharacterUpdate(UpdateView):
    model = Character
    fields = ['name']

class CharacterDelete(DeleteView):
    model = Character
    success_url = '/profile/'

class GameUpdate(UpdateView):
    model = Game
    fields = ['name', 'description']

class GameDelete(DeleteView):
    model = Game
    success_url = '/profile/'

