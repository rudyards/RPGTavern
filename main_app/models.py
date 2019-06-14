from django.db import models
from django.utils import timezone
from django.contrib.auth import user



# Create your models here.
class Proflie_photo(models.Model):
    url = models.CharField(max_length=300)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

class Game_photo(models.Model):
    url = models.CharField(max_length=300)
    game = models.ForeignKey(Gmae, on_delete=models.CASCADE)

class Character_photo(models.Model):
    url = models.CharField(max_length=300)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)

class Character_sheet_photo(models.Model):
    url = models.CharField(max_length=300)
    charactersheet = models.ForeignKey(charactersheet, on_delete=models.CASCADE)


class Like(models.Model):
    like = models.ArrayField()

class Meeting(models.Model):
    date = models.DateField(_("Date"), default=datetime.now())
    location = models.CharField(max_length=200)
    note = models.TextField(max_length=500)

class Comment(models.Model):
    content = models.TextField(max_length=150)
    date = models.DateField(_("Date"), default=datetime.now())
    like = models.OneToManyField(Like, on_delete=models.CASCADE)


class Game(models.Model):
    admin = models.ForeignKey(user, on_delete=models.CASCADE)
    game_photo = models.OneToOneField(Game_photo, on_delete=models.CASCADE)
    comment = models.OneToManyField(Comment, on_delete=models.CASCADE)
    meeting = models.OneToManyField(Meeting, on_delete=models.CASCADE)
    character = models.OneToManyField(Character, on_delete=models.CASCADE)

class Profile(models.Model):
    name = models.OneToOneField(name, on_delete=models.CASCADE)
    timezone = timezone.now
    profile_photo = models.OneToOneField(Proflie_photo, on_delete=models.CASCADE)
    game = models.OneToManyField(Game)





