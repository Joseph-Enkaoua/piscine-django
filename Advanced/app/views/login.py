from app.forms import LoginForm
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, resolve_url
from django.contrib import messages


class LoginFormView(FormView):
	template_name = "login.html"
	form_class = LoginForm
	success_url = reverse_lazy("app:articles")

	def form_valid(self, form):
		username = form.cleaned_data["username"]
		password = form.cleaned_data["password"]
		user = authenticate(username=username, password=password)
		if user is not None:
			login(self.request, user)
			next_url = self.request.GET.get("next", self.success_url)
			return HttpResponseRedirect(next_url)
		return self.form_invalid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# Provide fallback URL for Cancel button
		context["cancel_url"] = resolve_url("app:home")
		return context

class LoginNavFormView(FormView):
    form_class = LoginForm
    success_url = reverse_lazy("app:articles")

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            next_url = self.request.META.get("HTTP_REFERER", self.success_url)
            return redirect(next_url)
        return self.form_invalid(form)

    def form_invalid(self, _):
        messages.error(self.request, "Invalid username or password. Please try again.")
        referer_url = self.request.META.get("HTTP_REFERER", self.success_url)
        return redirect(referer_url)
