import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, RoomId
from django.contrib.auth.models import User


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        username = self.scope["user"]
        creator = User.objects.get(username=username)
        text_data_json = json.loads(text_data)
        message = str(text_data_json['message'])
        room = RoomId.objects.get(room_name=self.room_name)
        obj = Message(message=message, key=room, author=creator)
        obj.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'author': creator.username,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        author = event['author']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'author': author
        }))

    def call(self, event):
        # Receive message from room group
        message = event['message']
        caller = event['caller']
        calledto = event['calledto']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'call': message,
            'caller': caller,
            'calledto': calledto
        }))

    def order(self, event):
        self.send(text_data=json.dumps({
            'message': event['message']
        }))