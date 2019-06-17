
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from .models import Profile, Character, Game, Proflie_photo, Game_photo, Character_photo, Character_sheet_photo
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'taverntalk'

# Create your views here.
def home(request):
  return render(request, 'home.html')

def profile(request):
    return render(request, 'profile.html')

def add_Profile_photo(request, profile_id):
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
    fields = ['name', 'description']
