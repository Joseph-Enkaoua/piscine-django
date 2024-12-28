from django.urls import path

from chat.views import *

app_name = "chat"

urlpatterns = [
    path("<str:room_name>/", room_view, name="room"),
    path("", index_view, name="index"),
]
