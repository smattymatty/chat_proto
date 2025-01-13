from django.db import models
from django.contrib.auth import get_user_model
# Game Types
BASIC = 'basic'
ADVANCED = 'advanced'

# Game States
IN_QUEUE = 'in_queue'
MORNING = 'morning'
DAY = 'day'
NIGHT = 'night'
VOTING = 'voting'
class Game(models.Model):
    GAME_TYPE_CHOICES = [
        (BASIC, 'Basic'),
        (ADVANCED, 'Advanced'),
    ]
    GAME_STATE_CHOICES = [
        (IN_QUEUE, 'In Queue'),
        (MORNING, 'Morning'),
        (DAY, 'Day'),
        (NIGHT, 'Night'),
        (VOTING, 'Voting'),
    ]
    type = models.CharField(
        max_length=20,
        choices=GAME_TYPE_CHOICES,
        default=BASIC
    )
    name = models.CharField(max_length=128, unique=True)
    player_group = models.ForeignKey(
        'a_game.PlayerGroup',
        on_delete=models.CASCADE,
        related_name='players'
    )
    state = models.CharField(
        max_length=20,
        choices=GAME_STATE_CHOICES,
        default=IN_QUEUE
    )
    
    chat_room = models.ForeignKey(
        'a_chat.ChatRoom',
        on_delete=models.CASCADE,
        related_name='game'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
        
    class Meta:
        ordering = ['-created_at']

# Roles
INVESTIGATOR = 'investigator'
MURDERER = 'murderer'

class GamePlayer(models.Model):
    ROLE_CHOICES = [
        (INVESTIGATOR, 'Investigator'),
        (MURDERER, 'Murderer'),
    ]
    # parent models
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='game_players'
    )
    # game player attributes
    name = models.CharField(max_length=128)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=INVESTIGATOR
    )
    alive = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.name} the {self.role}'
        
        
class PlayerGroup(models.Model):
    player_1 = models.ForeignKey(
        GamePlayer,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='player_1'
    )
    player_2 = models.ForeignKey(
        GamePlayer,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='player_2'
    )
    player_3 = models.ForeignKey(
        GamePlayer,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='player_3'
    )
    player_4 = models.ForeignKey(
        GamePlayer,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='player_4'
    )
