import random
import time
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin


class RandomNameMiddleware(MiddlewareMixin):
  def process_request(self, request):
    if request.user.is_authenticated:
      request.session['username'] = request.user.username
    elif not request.session.get('last_name_update'):
      request.session['last_name_update'] = time.time()
      request.session['username'] = random.choice(settings.RANDOM_NAMES)
    else:
      last_update = request.session['last_name_update']
      if time.time() - last_update > 41:
        request.session['last_name_update'] = time.time()
        request.session['username'] = random.choice(settings.RANDOM_NAMES)


class RedirectIfAuthenticatedMixin(AccessMixin):
  """Mixin that redirects authenticated users to the homepage."""
    
  def dispatch(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      print("User is authenticated in login!")
      return redirect("home")
    return super().dispatch(request, *args, **kwargs)
