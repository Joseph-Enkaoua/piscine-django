from django.contrib import messages # type: ignore
from django.shortcuts import render, redirect # type: ignore
from .models import Movies

movies = [
  (1, 'The Phantom Menace', 'George Lucas', 'Rick McCallum', '1999-07-19'),
  (2, 'Attack of the Clones', 'George Lucas', 'Rick McCallum', '2002-07-16'),
  (3, 'Revenge of the Sith', 'George Lucas', 'Rick McCallum', '2007-07-19'),
  (4, 'A New Hope', 'George Lucas', 'Gary Kurtz, Rick McCallum', '1977-07-25'),
  (5, 'The Empire Strikes Back', 'Irvin Kershner', 'Gary Kurtz, Rick McCallum', '1980-07-17'),
  (6, 'Return of the Jedi', 'Richard Marquand', 'Howard G. Kazanjian, George Lucas, Rick McCallum', '1983-07-25'),
  (7, 'The Force Awakens', 'J. J. Abrams', 'Kathleen Kennedy, J. J. Abrams, Bryan Burk', '2015-12-11'),
]


def populate(request):
  for movie in movies:
    try:
      Movies.objects.create(
        episode_nb=movie[0],
        title=movie[1],
        director=movie[2],
        producer=movie[3],
        release_date=movie[4],
      )
      messages.success(request, f"OK - {movie[1]} added")
    except Exception as e:
      messages.error(request, f"KO - {movie[1]} - {e}")

  return render(request, 'ex07/display.html', {'title': 'Populate ex07'})


def display(request):
  try:
    movies = Movies.objects.all().order_by('episode_nb')
    return render(request, 'ex07/display.html', {'movies': movies, 'title': 'Display ex07'})
  except Exception:
    messages.error(request, "No data available")
    return render(request, 'ex07/display.html', {'title': 'Display ex07'})


def update(request):
  try:
    if request.method == 'POST':
      movie_to_remove = request.POST.get('movie')
      movie = Movies.objects.get(title=movie_to_remove)
      opening_crawl = request.POST.get('opening_crawl')
      if opening_crawl:
        movie.opening_crawl = opening_crawl
        movie.save()
      return redirect('/ex07/display')
    movies = Movies.objects.all().order_by('episode_nb')
    return render(request, 'ex07/update.html', {'movies': movies, 'title': 'Update ex07'})
  except Exception:
    messages.error(request, "No data available")
    return render(request, 'ex07/update.html', {'title': 'Update ex07'})
