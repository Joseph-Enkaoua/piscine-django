from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate
from .middleware import RedirectIfAuthenticatedMixin
from django.contrib.auth.views import LoginView
from .models import Tips
from .forms import TipForm

def index(request):
  tips = Tips.objects.all().order_by('-date')

  form = TipForm() if request.user.is_authenticated else None

  if request.method == 'POST' and request.user.is_authenticated:
    form = TipForm(request.POST)
    if form.is_valid():
      tip = form.save(commit=False)
      tip.author = request.user
      tip.save()
      return redirect('home')

  return render(request, 'home.html', {'tips': tips, 'form': form})


def get_username(request):
  username = request.session.get('username', 'Anonymous')
  return JsonResponse({'username': username})


class Register(RedirectIfAuthenticatedMixin, CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy("home")
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

    return redirect("home")


class CustomLoginView(RedirectIfAuthenticatedMixin, LoginView):
  template_name = "registration/login.html"

