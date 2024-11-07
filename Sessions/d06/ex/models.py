from django.contrib.auth.models import User
from django.db import models

class Tips(models.Model):
  class Meta:
    db_table = 'tips'

  content = models.TextField(max_length=2000)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  date = models.DateTimeField(auto_now_add=True, null=True)
  upvotes = models.ManyToManyField(User, related_name='upvotes')
  downvotes = models.ManyToManyField(User, related_name='downvotes')

  def __str__(self):
    return self.content
