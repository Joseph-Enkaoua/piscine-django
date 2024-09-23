from django.shortcuts import render # type: ignore
from .models import Movies
from django.http import HttpResponse # type: ignore


movies = [
  {
    'episode_nb': 1,
    'title': 'The Phantom Menace',
    'director': 'George Lucas',
    'producer': 'Rick McCallum',
    'release_date': '1999-05-19'
  },
  {
    'episode_nb': 2,
    'title': 'Attack of the Clones',
    'director': 'George Lucas',
    'producer': 'Rick McCallum',
    'release_date': '2002-05-16'
  },
  {
    'episode_nb': 3,
    'title': 'Revenge of the Sith',
    'director': 'George Lucas',
    'producer': 'Rick McCallum',
    'release_date': '2005-05-19'
  },
  {
    'episode_nb': 4,
    'title': 'A New Hope',
    'director': 'George Lucas',
    'producer': 'Gary Kurtz, Rick McCallum',
    'release_date': '1977-05-25'
  },
  {
    'episode_nb': 5,
    'title': 'The Empire Strikes Back',
    'director': 'Irvin Kershner',
    'producer': 'Gary Kurtz, Rick McCallum',
    'release_date': '1980-05-17'
  },
  {
    'episode_nb': 6,
    'title': 'Return of the Jedi',
    'director': 'Richard Marquand',
    'producer': 'Howard G. Kazanjian, George Lucas, Rick McCallum',
    'release_date': '1983-05-25'
  },
  {
    'episode_nb': 7,
    'title': 'The Force Awakens',
    'director': 'J.J. Abrams',
    'producer': 'Kathleen Kennedy, J.J. Abrams, Bryan Burk',
    'release_date': '2015-12-11'
  }
]


def populate(request):
  results = []
  for movie in movies:
    try:
      Movies.objects.update_or_create(
        title=movie['title'],
        defaults={
          'episode_nb': movie['episode_nb'],
          'director': movie['director'],
          'producer': movie['producer'],
          'release_date': movie['release_date']
        }
      )
      results.append("OK<br/>")
    except Exception as e:
      results.append(f"Error: {e}<br/>")

  return HttpResponse(results)


def display(request):
  try:
    movies = Movies.objects.all()
    if not movies:
      raise Movies.DoesNotExist
    return render(request, 'ex05/display.html', {'movies': movies})
  except Exception:
    return HttpResponse("No data available")


def remove(request):
  try:
    if request.method == 'POST':
      movie_to_remove = request.POST.get('movie')
      movie = Movies.objects.get(title=movie_to_remove)
      movie.delete()
    movies = Movies.objects.all()
    if not movies:
      raise Movies.DoesNotExist
    return render(request, 'ex05/remove.html', {'movies': movies})
  except Exception:
    return HttpResponse("No data available")