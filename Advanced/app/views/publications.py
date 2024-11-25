from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from app.models import Article


class PublicationsListView(LoginRequiredMixin, ListView):
    template_name = "publications.html"
    model = Article
    
    def get_queryset(self):
        """Filter articles to show only those authored by the logged-in user."""
        return Article.objects.filter(author=self.request.user).order_by("-created")
