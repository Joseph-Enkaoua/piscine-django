from django.db import models
from .user import *
from django.utils.translation import gettext_lazy as _


class Article(models.Model):
    title = models.CharField(max_length=64, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    created = models.DateTimeField(auto_now_add=True)
    synopsis = models.CharField(max_length=312)
    content = models.TextField()

    def __str__(self):
        return self.title

    @classmethod
    def create(cls, data):
        author = data.get("author")
        if not User.exists(author.username):
            raise ValueError(_("Author does not exist in the system"))

        return cls.objects.create(**data)

    @classmethod
    def exists(cls, title):
        return cls.objects.filter(title=title).exists()

    @classmethod
    def fetch(cls, title):
        return cls.objects.get(title=title)
