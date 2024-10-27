from django.urls import path

from . import views

urlpatterns = [
    path('api/get_username', views.get_username, name='Get Username'),
    path('', views.index, name='Home'),
]