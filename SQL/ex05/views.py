from django.contrib import messages # type: ignore
from django.shortcuts import render # type: ignore
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
      Movies.objects.update_or_create(
        title=movie[1],
        defaults={
          'episode_nb': movie[0],
          'director': movie[2],
          'producer': movie[3],
          'release_date': movie[4]
        }
      )
      messages.success(request, f"{movie['title']} added successfully")
    except Exception as e:
      messages.error(request, f"Error: {e}")

  return render(request, 'ex05/index.html', {'title': 'ex05 Populate'})


def display(request):
  try:
    movies = Movies.objects.all()
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