from django import forms
from django.contrib.auth.models import User
from .models import Game
from django.forms import ModelForm


class GameCreateForm(ModelForm):
    class Meta:
        model = Game
        fields = ['type']
        labels = {
            'type': 'Game Type',
        }
        widgets = {
            'type': forms.Select(choices=Game.GAME_TYPE_CHOICES),
        }