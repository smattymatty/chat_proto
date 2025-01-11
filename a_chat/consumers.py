import json

from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import AnonymousUser

from .models import *

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        # Get user, handling both authenticated and guest users
        user = self.scope["user"]
        if isinstance(user, AnonymousUser):
            # If no user is authenticated, check for guest session
            session = self.scope.get('session', {})
            guest_user_id = session.get('guest_user_id')
            if guest_user_id:
                try:
                    self.user = User.objects.get(id=guest_user_id)
                except User.DoesNotExist:
                    self.close()
                    return
            else:
                self.close()
                return
        else:
            self.user = user._wrapped if hasattr(user, "_wrapped") else user

        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatRoom, name=self.chatroom_name)
        
        # add this for channel layer
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,
            self.channel_name
        )
        
        # add and update online users
        if self.user not in self.chatroom.users_joined.all():
            self.chatroom.users_joined.add(self.user)
            self.update_online_count()
            
        self.accept()
        
    def disconnect(self, close_code):
        # to remove the channel from the group
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name, self.channel_name
        )
        # remove and update online users
        if self.user in self.chatroom.users_joined.all():
            self.chatroom.users_joined.remove(self.user)
            self.update_online_count()
        
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']
        
        message = ChatMessage.objects.create(
            body=body,
            author=self.user,
            room=self.chatroom,
        )
        event = {
            "type": "message_handler", # method name
            'message_id': message.id
        }
        # group_send replaces send, because we are broadcasting
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )
    # this handles the event sent by group_send
    def message_handler(self, event):
        message_id = event['message_id']
        message = ChatMessage.objects.get(id=message_id)
        context = {
            'message': message,
            'user': self.user,
        }
        html = render_to_string(
            'a_chat/partials/chat_message_p.html',
            context = context
        )
        self.send(text_data=html)
        
    def update_online_count(self):
        online_count = self.chatroom.users_joined.count()
        event = {
            'type': 'online_count_handler',
            'online_count': online_count
        }
        # broadcast to all users
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
            )
        
    def online_count_handler(self, event):
        online_count = event['online_count']
        html = render_to_string(
            'a_chat/partials/online_count.html',
            context = {
                'online_count': online_count,
                'chat_room': self.chatroom,
                }
        )
        self.send(text_data=html)