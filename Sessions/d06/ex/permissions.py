from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import AnonymousUser

class ReputationPermissionBackend(BaseBackend):
  def has_perm(self, user, perm, obj=None):
    if isinstance(user, AnonymousUser):
      return False  # Anonymous users don't have permissions

    # Grant delete_tips permission if the user has 30 or more reputation points
    if perm == "ex.delete_tips" and getattr(user, 'reputation', 0) >= 30:
      return True

    # Grant downvote permission if the user has 15 or more reputation points
    if perm == "downvote" and getattr(user, 'reputation', 0) >= 15:
      return True

    # Default to the original behavior for other permissions
    return super().has_perm(user, perm, obj)
