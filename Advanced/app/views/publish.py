from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from app.models import Article


class PublishArticleView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'content']
    template_name = "publish.html"
    success_url = reverse_lazy("app:publications")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
