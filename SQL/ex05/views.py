from django.contrib import messages # type: ignore
from django.shortcuts import render # type: ignore
from .models import Movies

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
      messages.success(request, f"{movie['title']} added successfully")
    except Exception as e:
      messages.error(request, f"Error: {e}")

  return render(request, 'ex05/index.html', {'title': 'ex05 Populate'})


def display(request):
  try:
    movies = Movies.objects.all()
    if not movies:
      raise Movies.DoesNotExist
    return render(request, 'ex05/index.html', {'movies': movies, 'title': 'ex05 Display'})
  except Exception:
    messages.error(request, "No data available")
    return render(request, 'ex05/index.html', {'title': 'ex05 Display'})


def remove(request):
  try:
    if request.method == 'POST':
      movie_to_remove = request.POST.get('movie')
      movie = Movies.objects.get(title=movie_to_remove)
      movie.delete()
    movies = Movies.objects.all()
    if not movies:
      raise Movies.DoesNotExist
    return render(request, 'ex05/remove.html', {'movies': movies, 'title': 'ex05 Remove'})
  except Exception:
    messages.error(request, "No data available")
    return render(request, 'ex05/remove.html', {'title': 'ex05 Remove'})