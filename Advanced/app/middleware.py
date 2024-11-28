from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin


class RedirectIfAuthenticatedMixin(AccessMixin):
  """Mixin that redirects authenticated users to the homepage."""
    
  def dispatch(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect("app:home")
    return super().dispatch(request, *args, **kwargs)
