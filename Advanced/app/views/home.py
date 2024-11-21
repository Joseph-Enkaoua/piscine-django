from django.urls import reverse_lazy
from django.views.generic.base import RedirectView

class HomeView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('app:articles')
