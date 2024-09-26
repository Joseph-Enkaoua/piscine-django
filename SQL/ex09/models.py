from django.db import models


class Planets(models.Model):
  class Meta:
    db_table = 'ex09_planets'

  name = models.CharField(max_length=64, unique=True, null=False)
  climate = models.CharField(max_length=255, blank=True, null=True)
  diameter = models.IntegerField(blank=True, null=True)
  orbital_period = models.IntegerField(blank=True, null=True)
  population = models.BigIntegerField(blank=True, null=True)
  rotation_period = models.IntegerField(blank=True, null=True)
  surface_water = models.FloatField(blank=True, null=True)
  terrain = models.TextField(blank=True, null=True)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self) -> str:
    return self.name


class People(models.Model):
  class Meta:
    db_table = 'ex09_people'

  name = models.CharField(max_length=64, null=False)
  birth_year = models.CharField(max_length=32, blank=True, null=True)
  gender = models.CharField(max_length=32, blank=True, null=True)
  eye_color = models.CharField(max_length=32, blank=True, null=True)
  hair_color = models.CharField(max_length=32, blank=True, null=True)
  height = models.IntegerField(blank=True, null=True)
  mass = models.FloatField(blank=True, null=True)
  homeworld = models.ForeignKey(Planets, on_delete=models.DO_NOTHING, null=True, max_length=64)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self) -> str:
    return self.name