from django import forms
from django.db.models import Min, Max
from .models import *


class SearchForm(forms.Form):
  min_release_date = forms.DateField(label='Movies Min Release Date', widget=forms.SelectDateWidget())
  max_release_date = forms.DateField(label='Movies Max Release Date', widget=forms.SelectDateWidget())
  min_diameter = forms.IntegerField(label='Planets Min Diameter')
  gender = forms.ChoiceField(label='Character gender', choices=[])

  def __init__(self, *args, **kwargs):
    super(SearchForm, self).__init__(*args, **kwargs)
    oldest_movie = Movies.objects.aggregate(Min('release_date'))['release_date__min']
    newest_movie = Movies.objects.aggregate(Max('release_date'))['release_date__max']
    if oldest_movie and newest_movie:
      min_year = oldest_movie.year
      max_year = newest_movie.year
      self.fields['min_release_date'].widget = forms.SelectDateWidget(years=range(min_year, max_year + 1))
      self.fields['max_release_date'].widget = forms.SelectDateWidget(years=range(min_year, max_year + 1))

    genders = People.objects.values_list('gender', flat=True).distinct()
    self.fields['gender'].choices = [(gender, gender) for gender in genders if gender]
