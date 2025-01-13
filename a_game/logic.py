from .models import Game, PlayerGroup, GamePlayer
from a_chat.models import ChatRoom
from django.db import IntegrityError
from secrets import token_urlsafe
import string

def create_game(user, game_type: str):
    if user.profile.is_guest:
        raise Exception("Guest users cannot create games")
    def get_game_name(user, game_type):
        return f"{game_type}-{user.username[0:1]}{token_urlsafe(9)}{user.username[-1:]}"
    try:
        # create the game's chat room
        new_chat_room = ChatRoom.objects.create(
            name=get_game_name(user, game_type),
        )
        # convert user into a GamePlayer
        new_game_player = GamePlayer.objects.create(
            user=user,
        )
        new_playerGroup = PlayerGroup.objects.create(
            player_1=new_game_player,
        )
        new_game = Game.objects.create(
            name=get_game_name(user, game_type),
            type=game_type,
            state='in_queue',
            chat_room=new_chat_room,
            player_group=new_playerGroup,
        )
        return new_game
    except Exception as e:
        # Clean up any objects that were created before the error
        if 'new_chat_room' in locals():
            new_chat_room.delete()
        if 'new_game_player' in locals():
            new_game_player.delete()
        if 'new_playerGroup' in locals():
            new_playerGroup.delete()
        return None
    
def update_game_state(
    game_name: int, state: str
    ) -> str:
    game = Game.objects.get(name=game_name)
    game.state = state
    game.save()

    return game.state