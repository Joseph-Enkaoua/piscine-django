from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import *
from .models import *


def index(request):
  username = request.session.get('username', 'Anonymous')
  return render(request, 'home.html', {'username': username})


def get_username(request):
  username = request.session.get('username', 'Anonymous')
  return JsonResponse({'username': username})


# def register(request):
#   form = RegisterForm()
#   if request.method == 'POST':
#     form = RegisterForm(request.POST)
#     if form.is_valid():
#       request.session['username'] = form.cleaned_data['username']
#       request.session['is_authenticated'] = True
#       user = form.save(commit=False)
#       user.set_password(form.cleaned_data['password'])
#       return render(request, 'main.html', {'username': form.cleaned_data['username']})
#   return render(request, 'register.html', {'form': form})