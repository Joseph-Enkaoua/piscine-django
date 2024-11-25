from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View


class LogoutView(View):
    """
    Logs the user out and redirects to the specified page.
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy("app:articles"))
