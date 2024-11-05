from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('api/get_username', views.get_username, name='Get Username'),
    path('register/', views.Register.as_view(), name='Register'),
    path('login/', views.CustomLoginView.as_view(), name='Login'),
    path('', views.index, name='Home'),
]