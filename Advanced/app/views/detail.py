from django.shortcuts import resolve_url
from django.views.generic import DetailView
from app.models import Article

class ArticleDetailView(DetailView):
    model = Article
    template_name = "article_detail.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Provide fallback URL for Cancel button
        context["cancel_url"] = resolve_url("app:home")
        return context