from django.db import models
from django.contrib.auth.models import User
from projects.models import Order

class RoomId(models.Model):
    user1 = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='user1')
    user2 = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='user2')
    room_name = models.CharField(max_length=128, unique=True)


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.ForeignKey(to=RoomId, on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)


class ChatFile(models.Model):
    name = models.CharField(max_length=600)
    file = models.FileField(blank=True, null=True, upload_to='messages/users/files')
    FileFrom = models.ForeignKey(User, related_name="file_from", on_delete=models.CASCADE)
    FileTo = models.ForeignKey(User, related_name="file_to", on_delete=models.CASCADE)

class VideoChat(models.Model):
    user1 = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='user1video')
    user2 = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='user2video')
    room_name = models.CharField(max_length=128, unique=True)

class Notify(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
class DeliverFiles(models.Model):
    name=models.CharField(max_length=600)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    file = models.FileField(blank=True, null=True, upload_to='messages/users/files')
    FileFrom = models.ForeignKey(User, related_name="deliverfile_from", on_delete=models.CASCADE)
    FileTo = models.ForeignKey(User, related_name="deliverfile_to", on_delete=models.CASCADE)