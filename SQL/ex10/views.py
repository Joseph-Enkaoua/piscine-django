from django.shortcuts import render # type: ignore
from .models import *
from .forms import *
from django.contrib import messages # type: ignore

def search(request):
  try:
    form = SearchForm(request.GET or None)
    if request.method == 'GET' and form.is_valid():
      min_release_date = form.cleaned_data.get('min_release_date')
      max_release_date = form.cleaned_data.get('max_release_date')
      min_diameter =  form.cleaned_data.get('min_diameter')
      gender = form.cleaned_data.get('gender')
      movies = Movies.objects.filter(
        release_date__range=(min_release_date, max_release_date),
        characters__gender=gender, characters__homeworld__diameter__gt=min_diameter,
      ).values_list('title', 'characters__name', 'characters__homeworld__name', 'characters__gender', 'characters__homeworld__diameter')
      if not movies:
        messages.error(request, 'No data found')
      return render(request, 'ex10/search.html', {'form': form, 'data': movies})

  except Exception as e:
    messages.error(request, 'Error: ' + str(e))
  return render(request, 'ex10/search.html', {'form': SearchForm()})

