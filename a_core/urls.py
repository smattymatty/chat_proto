from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('a_home.urls')),
    path('chat/', include('a_chat.urls')),
    path("accounts/", include("allauth.urls")),
    path('users/', include("a_users.urls")),
    path('game/', include('a_game.urls')),
]
