from django.urls import path
from . import views

urlpatterns = [
    path('api/get_username', views.get_username, name='get_username'),
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('', views.index, name='home'),
]