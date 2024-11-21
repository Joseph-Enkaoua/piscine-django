from django.urls import path
from .views import *

app_name = 'app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('home/', HomeView.as_view(), name='home'),
    path('articles/', ArticlesListView.as_view(), name='articles'),

    # path('register/', ViewRegister.as_view(), name='register'),
    # path('login/', ViewLogin.as_view(), name='login'),
    # path('login/nav/', ViewLoginNav.as_view(), name='login_nav'),
    # path('logout/', ViewLogout.as_view(), name='logout'),

    # path('publications/', ViewPublications.as_view(), name='publications'),
    # path('favourites/', ViewFavourites.as_view(), name='favourites'),
    # path('favourites/<int:pk>/add/', AddToFavouritesView.as_view(), name='favourites_add'),
    # path('details/<int:pk>/', ViewDetails.as_view(), name='details'),
    # path('publish/', ViewPublish.as_view(), name='publish'),

    # path('translate/', ViewTranslate.as_view(), name='translate'),
]

