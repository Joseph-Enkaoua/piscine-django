from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import UserFavoriteArticle, Article
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


class AddToFavoriteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['pk'])

        form = AddToFavForm(request.POST, user=request.user, article=article)
        if form.is_valid():
            UserFavoriteArticle.create(user=request.user, article=article)
            messages.success(self.request, _("Article added to favorites."))
            return redirect("app:article_detail", pk=self.kwargs['pk'])
        for error in form.non_field_errors():
            messages.error(request, error)
        return redirect("app:article_detail", pk=self.kwargs['pk'])
        
            
    model = UserFavoriteArticle
    form_class = AddToFavForm
    template_name = "add_to_favorite.html"
