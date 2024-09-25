from django.contrib import messages
from django.shortcuts import render
from .models import Movies


def populate(request):
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

  for movie in movies:
    try:
      Movies.objects.create(
        title=movie['title'],
        episode_nb=movie['episode_nb'],
        director=movie['director'],
        producer=movie['producer'],
        release_date=movie['release_date']
      )
      messages.success(request, f"OK, Movie {movie['title']} added")
    except Exception as e:
      messages.error(request, f"Error: {e}")

  return render(request, 'ex03/index.html', {'title': 'ex03 Populate'})

def display(request):
  try:
    movies = Movies.objects.all()
    if not movies:
        raise Movies.DoesNotExist
    return render(request, 'ex03/index.html', {'movies': movies, 'title': 'ex03 Display'})
  except:
    messages.error(request, "No data available")
    return render(request, 'ex03/index.html', {'title': 'ex03 Display'})
