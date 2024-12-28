from django.db import models
import django.contrib.auth as auth


class ChatRoom(models.Model):
  name = models.CharField(max_length=30, unique=True)
  users = models.ManyToManyField(auth.get_user_model(), related_name="rooms")

  def __str__(self):
    return self.name


class ChatMessage(models.Model):
  room = models.ForeignKey(ChatRoom, verbose_name="room", on_delete=models.CASCADE)
  user = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
  content = models.TextField()
  timestamp = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.content
