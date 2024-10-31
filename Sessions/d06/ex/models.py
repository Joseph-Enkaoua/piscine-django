# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# from django.db import models
# # from django.utils import timezone

# class CostumUser(AbstractBaseUser, PermissionsMixin):
#   username = models.CharField(max_length=150, unique=True)
#   # date_joined = models.DateTimeField(default=timezone.now)
#   # is_active = models.BooleanField(default=True)
#   # is_staff = models.BooleanField(default=False)

#   USERNAME_FIELD = 'username'
#   REQUIRED_FIELDS = []

#   def __str__(self):
#     return self.username