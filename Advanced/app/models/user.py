from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission

class User(AbstractBaseUser, PermissionsMixin):
  username = models.CharField(max_length=150, unique=True)

  groups = models.ManyToManyField(
    Group,
    related_name="custom_user_groups",
    blank=True,
    help_text="The groups this user belongs to.",
    verbose_name="groups",
  )
  user_permissions = models.ManyToManyField(
    Permission,
    related_name="custom_user_permissions",
    blank=True,
    help_text="Specific permissions for this user.",
    verbose_name="user permissions",
  )

  USERNAME_FIELD = "username"
  REQUIRED_FIELDS = []

  def __str__(self):
    return self.username

  @classmethod
  def create(cls, username, password=None, **extra_fields):
    if not username:
      raise ValueError('Username is required')
    user = cls(username=username, **extra_fields)
    user.set_password(password)
    user.save()
    return user

  @classmethod
  def exists(cls, username):
    return cls.objects.filter(username=username).exists()

  @classmethod
  def fetch(cls, username):
    return cls.objects.get(username=username)
