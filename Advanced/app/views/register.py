from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from app.forms import RegisterForm

class RegisterView(CreateView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("app:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        return super().form_valid(form)