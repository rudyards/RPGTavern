
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.views.generic.edit import CreateView
from .models import Profile, Meeting, Character, Game, Proflie_photo, Game_photo, Character_photo, Character_sheet_photo,Comment
from .forms import MeetingForm
from .forms import CommentForm

import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'taverntalk'
# Create your views here.
def home(request):
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
    for meeting in meetings:
        print(meeting[0].name)
    return render(request, 'profile.html',{'gmgames': gmgames, 'characters': characters, 'meetings': meetings, 'playergames': playergames})
  

def add_profile_photo(request, profile_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Proflie_photo(url=url, profile=profile_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('profile', profile=profile_id)


def add_character_photo(request, character_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Proflie_photo(url=url, character=character_id)
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
            photo = Proflie_photo(url=url, game=game_id)
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
    return render(request, 'characters/detail.html', {'character': character})
    

@login_required
def games_detail(request, game_id):
    game = Game.objects.get(id=game_id)
    comment = Comment.objects.all()
    comment_form = CommentForm()
    meetings = Meeting.objects.filter(game=game.id)
    meeting_form = MeetingForm()
    return render(request, 'games/detail.html', {'game': game, 'meeting_form': meeting_form, 'meetings': meetings, 'comment_form': comment_form, 'comment':comment})


def add_meeting(request, game_id):
    form = MeetingForm(request.POST)
    if form.is_valid():
        new_meeting = form.save(commit=False)
        new_meeting.game_id = game_id
        new_meeting.save()
    return redirect('games_detail', game_id=game_id)

def add_comment(request, game_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.game_id = game_id
        new_comment.save()
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
