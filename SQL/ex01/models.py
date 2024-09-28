from django.db import models


class Movies(models.Model):
  class Meta:
    db_table = 'ex01_movies'

  title = models.CharField(max_length=64, unique=True, null=False)
  episode_nb = models.IntegerField(primary_key=True)
  opening_crawl = models.TextField(blank=True, null=True)
  director = models.CharField(null=False, max_length=32)
  producer = models.CharField(null=False, max_length=128)
  release_date = models.DateField(null=False)

  def __str__(self) -> str:
    return self.title