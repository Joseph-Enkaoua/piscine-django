from django.db import models
from .user import *
from .article import *


class UserFavoriteArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'article')

    def __str__(self):
        return f"{self.user.username} - {self.article.title}"
    
    @classmethod
    def exists(cls, user, article):
        return cls.objects.filter(user=user, article=article).exists()
    
    @classmethod
    def create(cls, user, article):
        if cls.exists(user, article):
            raise Exception("Article is already in user's favorites list.")
        return cls.objects.create(user=user, article=article)
