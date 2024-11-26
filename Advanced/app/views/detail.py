from django.shortcuts import resolve_url
from django.views.generic import DetailView
from app.models import Article, UserFavoriteArticle
from app.forms import AddToFavForm


class ArticleDetailView(DetailView):
    model = Article
    template_name = "article_detail.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Provide fallback URL for Cancel button
        context["cancel_url"] = resolve_url("app:home")

        if self.request.user.is_authenticated:
            # Check if the article is already in the user's favorites
            context["is_favorited"] = UserFavoriteArticle.exists(self.request.user, self.object)
            article = self.get_object()
            form = AddToFavForm(user=self.request.user, article=article)
            context["form"] = form
        return context