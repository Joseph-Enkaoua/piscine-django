from django.shortcuts import render # type: ignore
from .models import People
from django.contrib import messages # type: ignore

def display(request):
  people = People.objects.filter(homeworld__climate__icontains='windy').values_list('name', 'homeworld__name', 'homeworld__climate').order_by('name')
  if len(people) == 0:
    messages.error(request, 'No data available, please use the following command line before use: python -B manage.py loaddata ex09/data/ex09_initial_data.json')
    messages.error(request, 'then, run the following command: python3 manage.py runserver')
  return render(request, 'ex09/display.html', {'people': people, 'title': 'People from windy planets'})

