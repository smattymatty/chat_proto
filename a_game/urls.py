from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.game_home, name='home'),
    path('play/<str:game_name>/', views.play_game, name='play'),
    # htmx routes
    path('update_state/<str:game_name>/', views.update_game_state_view, name='update_state'),
    path('list/<str:started>/', views.game_list, name='list'),
]