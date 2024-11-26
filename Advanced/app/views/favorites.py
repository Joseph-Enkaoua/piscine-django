from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import UserFavouriteArticle
from django.views.generic.edit import CreateView


class FavouritesListView(LoginRequiredMixin, ListView):
    template_name = "favourites.html"
    context_object_name = "favorite_articles"

    def get_queryset(self):
        # Filter UserFavouriteArticle for the logged-in user and return related articles
        return UserFavouriteArticle.objects.filter(user=self.request.user).select_related('article')


class AddToFavouriteView(LoginRequiredMixin, CreateView):
    model = UserFavouriteArticle
    fields = []
    template_name = "add_to_favourite.html"
    success_url = reverse_lazy("app:favourites")

    def form_valid(self, form):
        article_id = self.kwargs["pk"]
        form.instance.article_id = article_id
        form.instance.user = self.request.user
        return super().form_valid(form)