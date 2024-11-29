from django.db import IntegrityError
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import UserFavoriteArticle, Article
from django.views.generic.edit import CreateView
from app.forms import AddToFavForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class FavoritesListView(LoginRequiredMixin, ListView):
    template_name = "favorites.html"
    context_object_name = "favorite_articles"

    def get_queryset(self):
        # Filter UserFavoriteArticle for the logged-in user and return related articles
        return UserFavoriteArticle.objects.filter(user=self.request.user).select_related('article')


class AddToFavoriteView(LoginRequiredMixin, CreateView):
    model = UserFavoriteArticle
    form_class = AddToFavForm
    template_name = "add_to_favorite.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        article = get_object_or_404(Article, pk=self.kwargs['pk'])
        kwargs['user'] = self.request.user
        kwargs['article'] = article
        return kwargs

    def form_valid(self, form):
        try:
            form.save()
        except IntegrityError:
            messages.error(self.request, _("Error: Article is already in your favorites."))
        return redirect("app:article_detail", pk=self.kwargs['pk'])
