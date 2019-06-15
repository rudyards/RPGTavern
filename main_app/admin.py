from django.contrib import admin
from .models import Game, Character, Meeting, Comment

# Register your models here.
admin.site.register(Game)
admin.site.register(Character)
admin.site.register(Meeting)
admin.site.register(Comment)