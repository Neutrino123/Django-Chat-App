from django.db import models
import uuid
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(null=True, blank=False, max_length=200)
    friends = models.ManyToManyField('self', blank=True)
    bio = models.TextField(null=True, blank=True, max_length=500)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
  
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)

class FriendRequest(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_friend_requests')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_friend_requests')
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.sender.username)

    class Meta:
        unique_together = [['sender', 'receiver']]

class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    body = models.TextField(null=False, blank=False)
    seen = models.BooleanField(default=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.body)
    
