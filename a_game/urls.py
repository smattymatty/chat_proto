from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.game_home, name='home'),
    path('play/<str:game_name>/', views.play_game, name='play'),
]