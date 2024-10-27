from django.http import JsonResponse
from django.shortcuts import render


def index(request):
  username = request.session.get('username', 'Anonymous')
  return render(request, 'main.html', {'username': username})

def get_username(request):
  username = request.session.get('username', 'Anonymous')
  return JsonResponse({'username': username})
