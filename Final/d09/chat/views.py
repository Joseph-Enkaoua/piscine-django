from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages


@login_required
def index_view(request):
  rooms = ChatRoom.objects.all().order_by("name")
  return render(request, "index.html", { "rooms": rooms })


@login_required
def room_view(request, room_name):
  try:
    room = ChatRoom.objects.get(name=room_name)
  except ChatRoom.DoesNotExist:
    messages.error(request, "The chat room does not exist.")
    return redirect("chat:index")
  return render(request, "room.html", { "room": room })
