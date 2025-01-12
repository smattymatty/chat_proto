from django.shortcuts import render, redirect
from .models import Game
from .forms import GameCreateForm
from .logic import create_game



# Create your views here.
def game_home(request):
    template = 'a_game/find_game.html'
    
    if request.method == 'POST':
        print(f"Form Post: {request.POST}")
        form = GameCreateForm(request.POST)
        if form.is_valid():
            post_data = form.cleaned_data
            game_type = post_data['type']
            new_game = create_game(request.user, game_type)
            
            if new_game:
                print(f"New Game: {new_game}")
                return redirect('game:play', game_name=new_game.name)
            else:
                # Handle game creation failure
                form.add_error(None, "Failed to create game. Please try again.")
        else:
            print(f"Form Errors: {form.errors}")
    
    form = GameCreateForm()
    games = Game.objects.all().filter(state='in_queue')
    context = {
        'games': games,
        'form': form,
    }
    return render(request, template, context)

def play_game(request, game_name):
    template = 'a_game/play_game.html'
    game = Game.objects.get(name=game_name)
    chat_room = game.chat_room
    context = {
        'game': game,
        'chat_room': chat_room,
    }
    return render(request, template, context)