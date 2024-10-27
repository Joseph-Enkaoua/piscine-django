import random
import time
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class RandomNameMiddleware(MiddlewareMixin):
  def process_request(self, request):
    if not request.session.get('last_name_update'):
      request.session['last_name_update'] = time.time()
      request.session['username'] = random.choice(settings.RANDOM_NAMES)
    else:
      last_update = request.session['last_name_update']
      if time.time() - last_update > 42:
        request.session['last_name_update'] = time.time()
        request.session['username'] = random.choice(settings.RANDOM_NAMES)