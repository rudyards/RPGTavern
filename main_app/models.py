from django.db import models
from django.utils import timezone
from datetime import date, datetime
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timezone = timezone.now

class Game(models.Model):
    name = models.CharField(max_length=300)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)

class Character(models.Model):
    name = models.CharField(max_length=100)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField('Date', default=datetime.now())

    def get_absolute_url(self):
        print('hitting')
        return reverse('characters_detail', kwargs={'character_id': self.id})

class Meeting(models.Model):
    date = models.DateField('Date')
    location = models.CharField(max_length=200)
    note = models.TextField(max_length=500)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

class Comment(models.Model):
    content = models.TextField(max_length=150)
    date = models.DateField('Date')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)



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
    




