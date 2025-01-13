from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed, HttpRequest, HttpResponse

from .models import Game
from .forms import GameCreateForm
from .logic import create_game, update_game_state



# Create your views here.
def game_home(request: HttpRequest):
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
                print(f"Form Errors: {form.errors}")
                return redirect('game:home')
        else:
            print(f"Form Errors: {form.errors}")
    if not request.user.profile.is_guest:
        form = GameCreateForm()
    else:
        form = ""
    games = Game.objects.all().filter(state='in_queue')
    context = {
        'games': games,
        'form': form,
    }
    return render(request, template, context)

def game_list(request, started: str):
    print(f"Game List: {started}")
    template = 'a_game/partials/game_list.html'
    if started == 'false':
        games = Game.objects.all().filter(state='in_queue')
    else:
        # any game thats NOT in the queue
        games = Game.objects.all().filter(state__in=['morning', 'day', 'night', 'voting'])
    context = {
        'games': games,
        'started': started,
    }
    return render(request, template, context)
    
def play_game(request, game_name: str):
    template = 'a_game/play_game.html'
    game = Game.objects.get(name=game_name)
    chat_room = game.chat_room
    context = {
        'game': game,
        'chat_room': chat_room,
    }
    return render(request, template, context)

def update_game_state_view(request, game_name: str):
    if request.method == 'POST':
        try:
            # get the post data
            post_data = request.POST
            game = Game.objects.get(name=game_name)
            # validate the post data
            if 'state' not in post_data:
                raise Exception("Invalid post data: state not found")
            state = post_data['state']
            try:
                new_state = update_game_state(game, state)
                return render(request, 'a_game/partials/game_state.html', {
                    'game': game,
                    'state': new_state,
                    })
            except Exception as e:
                print(f"Error updating game state: {str(e)}")
            # any other logic or data needed to be updated
            # alive players, day_
        except Exception as e:
            print(f"Error updating game state: {str(e)}")
            return HttpResponseNotAllowed(['POST'])