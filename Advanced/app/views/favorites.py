from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import UserFavouriteArticle


class FavouritesListView(LoginRequiredMixin, ListView):
    template_name = "favourites.html"
    context_object_name = "favorite_articles"

    def get_queryset(self):
        # Filter UserFavouriteArticle for the logged-in user and return related articles
        return UserFavouriteArticle.objects.filter(user=self.request.user).select_related('article')
