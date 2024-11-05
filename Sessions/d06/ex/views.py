from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate
from .middleware import RedirectIfAuthenticatedMixin
from django.contrib.auth.views import LoginView

def index(request):
  username = request.session.get('username', 'Anonymous')
  return render(request, 'home.html', {'username': username})


def get_username(request):
  username = request.session.get('username', 'Anonymous')
  return JsonResponse({'username': username})


class Register(RedirectIfAuthenticatedMixin, CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy("Home")
  template_name = "registration/register.html"

  def form_valid(self, form):
    user = form.save()

    user = authenticate(
      self.request,
      username=form.cleaned_data.get("username"),
      password=form.cleaned_data.get("password1")
    )
    if user is not None:
      login(self.request, user)
    else:
      print("User authentication failed")

    return redirect("Home")

class CustomLoginView(RedirectIfAuthenticatedMixin, LoginView):
  template_name = "registration/login.html"