from django.urls import path
from .views import *

app_name = "app"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("home/", HomeView.as_view(), name="home"),
    path("articles/", ArticlesListView.as_view(), name="articles"),
    path("login/", LoginFormView.as_view(), name="login"),
    path("publications/", PublicationsListView.as_view(), name="publications"),
    path("detail/<int:pk>/", ArticleDetailView.as_view(), name="article_detail"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # path('register/', ViewRegister.as_view(), name='register'),
    # path('login/nav/', ViewLoginNav.as_view(), name='login_nav'),
    # path('favourites/', ViewFavourites.as_view(), name='favourites'),
    # path('favourites/<int:pk>/add/', AddToFavouritesView.as_view(), name='favourites_add'),
    # path('publish/', ViewPublish.as_view(), name='publish'),
    # path('translate/', ViewTranslate.as_view(), name='translate'),
]
