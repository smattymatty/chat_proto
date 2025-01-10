from django.forms import ModelForm
from django import forms

from .models import *

class ChatMessageCreateForm(ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['body']
        labels = {
            'body': '',
        }
        widgets = {
            'body': forms.TextInput(
                attrs={
                    'placeholder': 'Add message ...', 
                    'class': 'sb-p-2 sb-black sb-w-full', 
                    'maxlength': '300', 
                    'autofocus': True}),
        }
        
class ChatRoomCreateForm(ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        return name.replace(' ', '_')
    
    class Meta:
        model = ChatRoom
        fields = ['name']
        labels = {'name': ''}
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'New Room Name', 
                    'class': 'sb-p-2 sb-black', 
                    'maxlength': '32', 
                    'autofocus': True}),
            
        }