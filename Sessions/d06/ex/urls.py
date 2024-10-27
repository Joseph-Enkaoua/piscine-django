from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='Home'),
    path('api/get_username', views.get_username, name='Get Username'),
]