from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    name = models.CharField(max_length=128, unique=True)
    users_joined = models.ManyToManyField(
        User,
        related_name='users_joined',
        blank=True
    )
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"Room {self.id}"
            
        self.name.replace(" ", "_")
        return super().save(*args, **kwargs)
    
class ChatMessage(models.Model):
    room = models.ForeignKey(
        ChatRoom,
        related_name="messages",
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    body= models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.author.username}: {self.body}'
    
    class Meta:
        ordering = ['-created_at']