from django.views.generic import ListView
from app.models import *


class ArticlesListView(ListView):
    template_name = "articles.html"
    model = Article
    queryset = Article.objects.filter().order_by("-created")
