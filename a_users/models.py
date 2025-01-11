from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    info = models.TextField(null=True, blank=True) 
    is_guest = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.user)