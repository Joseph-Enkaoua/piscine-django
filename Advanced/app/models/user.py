from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission, BaseUserManager

class CustomUserManager(BaseUserManager):
  def create_user(self, username, password=None, **extra_fields):
    if not username:
        raise ValueError("The Username field must be set")
    user = self.model(username=username, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, username, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)

    if extra_fields.get('is_staff') is not True:
        raise ValueError("Superuser must have is_staff=True.")
    if extra_fields.get('is_superuser') is not True:
        raise ValueError("Superuser must have is_superuser=True.")

    return self.create_user(username, password, **extra_fields)

  def get_by_natural_key(self, username):
    return self.get(username=username)


class User(AbstractBaseUser, PermissionsMixin):
  username = models.CharField(max_length=150, unique=True)
  is_staff = models.BooleanField(default=False)  # Required for admin access
  is_active = models.BooleanField(default=True)  # Required for login

  # Attach the custom manager
  objects = CustomUserManager()

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
