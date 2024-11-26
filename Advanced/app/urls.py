from django.urls import path
from .views import *

app_name = "app"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("home/", HomeView.as_view(), name="home"),
    path("articles/", ArticlesListView.as_view(), name="articles"),
    path("login/", LoginFormView.as_view(), name="login"),
    path("login/nav", LoginNavFormView.as_view(), name="login_nav"),
    path("publications/", PublicationsListView.as_view(), name="publications"),
    path("detail/<int:pk>/", ArticleDetailView.as_view(), name="article_detail"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("favorites/", FavoritesListView.as_view(), name="favorites"),
    path("register/", RegisterView.as_view(), name="register"),
    path("publish/", PublishArticleView.as_view(), name="publish"),
    path("add-to-favorite/<int:pk>/", AddToFavoriteView.as_view(), name="add_to_favorite"),
]