from django.db import models
from user_auth.models import User

class ConnversationRoom(models.Model):
    pass

class AIUser(models.Model):
    pass

class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()