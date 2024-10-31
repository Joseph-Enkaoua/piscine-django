from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('api/get_username', views.get_username, name='Get Username'),
    # path('register/', views.register, name='Register'),
    path('', views.index, name='Home'),
]