from django.contrib import admin
from .models import Game, Character, Meeting, Comment, Proflie_photo, Game_photo, Character_photo, Character_sheet_photo

# Register your models here.
admin.site.register(Game)
admin.site.register(Character)
admin.site.register(Meeting)
admin.site.register(Comment)
admin.site.register(Proflie_photo)
admin.site.register(Game_photo)
admin.site.register(Character_photo)
admin.site.register(Character_sheet_photo)