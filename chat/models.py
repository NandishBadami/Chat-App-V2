from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')

    def __str__(self):
        return self.friend.username

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    text = models.TextField()
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def update(self):
        self.read = True