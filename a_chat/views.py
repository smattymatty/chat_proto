from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .forms import ChatMessageCreateForm, ChatRoomCreateForm
from .models import ChatRoom

def chat_home(request, room_name):
    context = {
        'chat_room': ChatRoom.objects.get(name=room_name),
    }
    return render(request, 'home.html', context)

def chat_list(request):
    form = ChatRoomCreateForm()
    if request.method == 'POST':
        form = ChatRoomCreateForm(request.POST)
        if form.is_valid():
            chat_room = form.save()
            return redirect('chat:chat_home', room_name=chat_room.name)
    chat_rooms = ChatRoom.objects.all()
    context = {
        'chat_rooms': chat_rooms,
        'form': form
    }
    return render(request, 'a_chat/chat_list.html', context)

@login_required
def open_chatroom(request, room_name):
    template = 'a_chat/chat_room.html'
    
    chat_room = get_object_or_404(ChatRoom, name=room_name)
    messages = chat_room.messages.all()[:30]
    print(f"Chat Room: {chat_room}")
    form = ChatMessageCreateForm()
    
    if request.method == 'POST':
        print(f"Form POST: {form.is_valid()}")
        form = ChatMessageCreateForm(request.POST)
        if form.is_valid():
            print(f"Form Valid: {form.is_valid()}")
            message = form.save(commit=False)
            message.author = request.user
            message.room = chat_room
            message.save()
            print(f"Message Saves: {message}")
            context = {
                'message': message,
                'user': request.user,
            }
            return render(
                request, 'a_chat/partials/chat_message_p.html', context
                )
        else:
            print(f"Form Errors: {form.errors}")
    context = {
        'chat_room': chat_room,
        'messages': messages,
        'form': form,
        'user': request.user,
    }
    return render(request, template, context)

def online_count(request, room_name):
    template = 'a_chat/partials/online_count.html'
    room = ChatRoom.objects.get(name=room_name)
    online_count = room.users_joined.count()
    context = {
        'online_count': online_count,
    }
    return render(request, template, context)