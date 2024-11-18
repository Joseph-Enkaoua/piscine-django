from django.db.models.signals import post_delete
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count
from django.dispatch import receiver

class CustomUser(AbstractUser):
  reputation = models.IntegerField(default=0)

  def update_reputation(self):
    reputation = 0
    tips = self.tips_set.annotate(
      upvotes_count=Count('upvotes')
    )
    for tip in tips:
      reputation += (tip.upvotes_count or 0) * 5
    
    tips = self.tips_set.annotate(
      downvotes_count=Count('downvotes')
    )
    for tip in tips:
      reputation -= (tip.downvotes_count or 0) * 2

    self.reputation = reputation
    self.save()

  
class Tips(models.Model):
  class Meta:
    db_table = 'tips'
    permissions = [
      ("downvote", "Can downvote tips"),
    ]

  content = models.TextField(max_length=2000)
  author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  date = models.DateTimeField(auto_now_add=True, null=True)
  upvotes = models.ManyToManyField(CustomUser, related_name='upvotes')
  downvotes = models.ManyToManyField(CustomUser, related_name='downvotes')

  def __str__(self):
    return self.content


@receiver(post_delete, sender=Tips)
def update_author_reputation_on_delete(sender, instance, **kwargs):
  instance.author.update_reputation()