from django import forms
from app.models import UserFavoriteArticle
from django.utils.translation import gettext_lazy as _


class AddToFavForm(forms.ModelForm):
    class Meta:
        model = UserFavoriteArticle
        fields = []

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.article = kwargs.pop('article')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if UserFavoriteArticle.exists(self.user, self.article):
            raise forms.ValidationError(_("This article is already in your favorites."))
        return cleaned_data
