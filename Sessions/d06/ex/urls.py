from django.urls import path
from . import views

urlpatterns = [
    path('api/get_username', views.get_username, name='get_username'),
    path('api/delete_tip<int:tip_id>', views.delete_tip, name='delete_tip'),
    path('api/upvote_tip/<int:tip_id>/', views.upvote_tip, name='upvote_tip'),
    path('api/downvote_tip/<int:tip_id>/', views.downvote_tip, name='downvote_tip'),
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('', views.index, name='home'),
]