from django.db import models
from django.utils import timezone
from datetime import date, datetime
from django.contrib.auth.models import User



# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timezone = timezone.now


class Game(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)

class Character(models.Model):
    name = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    date = models.DateField('Date', default=datetime.now())

class Proflie_photo(models.Model):
    url = models.CharField(max_length=300)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

class Game_photo(models.Model):
    url = models.CharField(max_length=300)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

class Character_photo(models.Model):
    url = models.CharField(max_length=300)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)

class Character_sheet_photo(models.Model):
    url = models.CharField(max_length=300)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    


class Meeting(models.Model):
    date = models.DateField('Date')
    location = models.CharField(max_length=200)
    note = models.TextField(max_length=500)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

class Comment(models.Model):
    content = models.TextField(max_length=150)
    date = models.DateField('Date', default=datetime.now())
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


