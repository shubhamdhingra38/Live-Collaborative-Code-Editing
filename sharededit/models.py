from django.db import models
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    room_name = models.CharField(max_length=20, unique=True)
    chat_users = models.ManyToManyField('ChatUser', through='UserAndRoom')
    room_password = models.CharField(max_length=50)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return self.room_name

# Create your models here.
class ChatUser(models.Model):
    chat_user = models.OneToOneField(User, on_delete=models.CASCADE)
    chat_rooms = models.ManyToManyField('ChatRoom', through='UserAndRoom')

    def __str__(self):
        return self.chat_user.username

class UserAndRoom(models.Model):
    chat_user = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'u({str(self.chat_user)})-r({str(self.chat_room)})'
    