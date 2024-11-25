from django.views.generic import DetailView
from app.models import Article

class ArticleDetailView(DetailView):
    model = Article
    template_name = "article_detail.html"
    context_object_name = "article"
