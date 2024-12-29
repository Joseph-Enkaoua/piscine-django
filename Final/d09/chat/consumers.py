import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import *
import django.contrib.auth

class ChatConsumer(WebsocketConsumer):
  def connect(self):
    if not self.scope["user"].is_authenticated:
      self.close()
      return

    self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
    self.room_group_name = f"chat_{self.room_name}"
    
    try:
      self.room = ChatRoom.objects.get(name=self.room_name)
      User = django.contrib.auth.get_user_model()
      self.user = User.objects.get(username=self.scope["user"])
    except ChatRoom.DoesNotExist:
      self.close
      return
    
    self.room.users.add(self.scope["user"])

    async_to_sync(self.channel_layer.group_add)(
      self.room_group_name, self.channel_name
    )

    self.accept()

    message = self.user.username + " has joined the chat"
    async_to_sync(self.channel_layer.group_send)(
      self.room_group_name, {"type": "chat.message", "message": message, "user": "system" }
    )


  def disconnect(self, code):
    async_to_sync(self.channel_layer.group_discard)(
      self.room_group_name, self.channel_name
    )

    self.room.users.remove(self.scope["user"])

    message = self.user.username + " has left the chat"
    async_to_sync(self.channel_layer.group_send)(
      self.room_group_name, {"type": "chat.message", "message": message, "user": "system" }
    )


  def receive(self, text_data):
    text_data_json = json.loads(text_data)
    message = text_data_json["message"]

    async_to_sync(self.channel_layer.group_send)(
      self.room_group_name, {"type": "chat.message", "message": message, "user": self.user.username }
    )

    ChatMessage.objects.create(room=self.room, user=self.user, content=message)


  def chat_message(self, event):
    message = event["message"]
    user = event["user"]

    self.send(text_data=json.dumps({"message": message, "user": user}))
