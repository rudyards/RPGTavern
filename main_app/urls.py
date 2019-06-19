from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile_page'),
    path('profile/add_photo/', views.add_profile_photo, name='profile_photo'),
    path('characters/<int:character_id>/', views.characters_detail, name='characters_detail'),
    path('characters/create/', views.CharacterCreate.as_view(), name='characters_create'),
    path('characters/<int:pk>/update/', views.CharacterUpdate.as_view(), name='characters_update'),
    path('characters/<int:pk>/delete/', views.CharacterDelete.as_view(), name='characters_delete'),
    path('characters/<int:character_id>/add_photo/', views.add_character_photo, name='character_photo'),
    path('characters/<int:character_id>/add_cs_photo/', views.add_character_sheet_photo, name='character_sheet_photo'),
    path('games/<int:game_id>/', views.games_detail, name='games_detail'),
    path('games/<int:game_id>/add_meeting/', views.add_meeting, name='add_meeting'),
    path('games/<int:game_id>/add_comment/', views.add_comment, name='add_comment'),
    path('games/<int:game_id>/add_photo/', views.add_game_photo, name='game_photo'),
    path('games/create/', views.GameCreate.as_view(), name='games_create'),
    path('games/<int:pk>/update/', views.GameUpdate.as_view(), name='games_update'),
    path('games/<int:pk>/delete/', views.GameDelete.as_view(), name='games_delete'),
    path('games/<int:game_id>/join/', views.games_join, name='games_join'),
]