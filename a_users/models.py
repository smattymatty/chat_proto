from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    info = models.TextField(null=True, blank=True) 
    
    def __str__(self):
        return str(self.user)