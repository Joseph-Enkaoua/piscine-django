from django.db import models
from .user import *

class Article(models.Model):
  title = models.CharField(max_length=64, unique=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  created = models.DateTimeField(auto_now_add=True)
  synopsis = models.CharField(max_length=312)
  content = models.TextField()

  def __str__(self):
    return self.title