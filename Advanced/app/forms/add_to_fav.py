from django import forms
from app.models import UserFavoriteArticle


class AddToFavForm(forms.ModelForm):
    class Meta:
        model = UserFavoriteArticle
        fields = []

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.article = kwargs.pop('article')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        favorite = super().save(commit=False)
        favorite.user = self.user
        favorite.article = self.article
        if commit:
            favorite.save()
        return favorite
