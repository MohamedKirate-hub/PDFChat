from django.db import models
from user_auth.models import User
import uuid 

def genarate_uuid():
    return str(uuid.uuid4())

class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
            ordering = ["-created_at"]

class ConversationRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rooms")
    created_at = models.DateTimeField(auto_now_add=True)

class Conversation(models.Model):
    title = models.CharField(max_length=150, default=genarate_uuid)
    room = models.ForeignKey(ConversationRoom, on_delete=models.CASCADE, related_name="conversations")
    conversations = models.ManyToManyField(Message)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.title
