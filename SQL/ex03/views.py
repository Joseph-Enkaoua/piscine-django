from django.contrib import messages
from django.shortcuts import render
from .models import Movies

movies = [
  (1, 'The Phantom Menace', 'George Lucas', 'Rick McCallum', '1999-05-19'),
  (2, 'Attack of the Clones', 'George Lucas', 'Rick McCallum', '2002-05-16'),
  (3, 'Revenge of the Sith', 'George Lucas', 'Rick McCallum', '2005-05-19'),
  (4, 'A New Hope', 'George Lucas', 'Gary Kurtz, Rick McCallum', '1977-05-25'),
  (5, 'The Empire Strikes Back', 'Irvin Kershner', 'Gary Kurtz, Rick McCallum', '1980-05-17'),
  (6, 'Return of the Jedi', 'Richard Marquand', 'Howard G. Kazanjian, George Lucas, Rick McCallum', '1983-05-25'),
  (7, 'The Force Awakens', 'J.J. Abrams', 'Kathleen Kennedy, J.J. Abrams, Bryan Burk', '2015-12-11')
]


def populate(request):
  for movie in movies:
    try:
      Movies.objects.create(
        episode_nb=movie[0],
        title=movie[1],
        director=movie[2],
        producer=movie[3],
        release_date=movie[4]
      )
      messages.success(request, f"OK, Movie {movie[1]} added")
    except Exception as e:
      messages.error(request, f"Error: {e}")

  return render(request, 'ex03/index.html', {'title': 'ex03 Populate'})


def display(request):
  try:
    movies = Movies.objects.all()
    if not movies:
      raise Exception()
    return render(request, 'ex03/index.html', {'movies': movies, 'title': 'ex03 Display'})
  except:
    messages.error(request, "No data available")
    return render(request, 'ex03/index.html', {'title': 'ex03 Display'})
