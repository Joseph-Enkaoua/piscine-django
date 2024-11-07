from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate
from .middleware import RedirectIfAuthenticatedMixin
from django.contrib.auth.views import LoginView
from .models import Tips
from .forms import TipForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

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

  can_delete_tips = request.user.has_perm("ex.delete_tips")
  return render(request, 'home.html', {'tips': tips, 'form': form, 'can_delete_tips': can_delete_tips})


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


@login_required
def delete_tip(request, tip_id):
  tip = get_object_or_404(Tips, id=tip_id)
  
  if request.user == tip.author or request.user.has_perm('ex.delete_tips'):
    tip.delete()
    return redirect('home')
  else:
    raise PermissionDenied


@login_required
def upvote_tip(request, tip_id):
  tip = get_object_or_404(Tips, id=tip_id)
  if request.user in tip.upvotes.all():
    tip.upvotes.remove(request.user)
  else:
    tip.upvotes.add(request.user)
    tip.downvotes.remove(request.user)
  tip.save()
  return redirect('home')


@login_required
def downvote_tip(request, tip_id):
  tip = get_object_or_404(Tips, id=tip_id)
  if request.user in tip.downvotes.all():
    tip.downvotes.remove(request.user)
  else:
    tip.downvotes.add(request.user)
    tip.upvotes.remove(request.user)
  tip.save()
  return redirect('home')
