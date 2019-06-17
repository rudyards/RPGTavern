from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile_page'),
    path('characters/<int:character_id>/', views.characters_detail, name='characters_detail'),
    path('characters/create/', views.CharacterCreate.as_view(), name='characters_create'),
    path('games/<int:game_id>/', views.games_detail, name='games_detail'),
    path('games/create/', views.GameCreate.as_view(), name='games_create'),
]