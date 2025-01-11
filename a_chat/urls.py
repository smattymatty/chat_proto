from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'chat'

urlpatterns = [
    path('join/<str:room_name>/', views.chat_home, name='chat_home'),
    path('list/', views.chat_list, name='chat_list'),
    path('chatroom/<str:room_name>/', views.open_chatroom, name='open_chatroom'),
    path('online_count/<str:room_name>/', views.online_count, name='online_count'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)