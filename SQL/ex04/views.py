from django.contrib import messages
from django.shortcuts import render
import psycopg2
from django.conf import settings
from django.views.decorators.http import require_http_methods

movies = [
  {
    "episode_nb": 1,
    "title": "The Phantom Menace",
    "director": "George Lucas",
    "producer": "Rick McCallum",
    "release_date": "1999-05-19",
  },
  {
    "episode_nb": 2,
    "title": "Attack of the Clones",
    "director": "George Lucas",
    "producer": "Rick McCallum",
    "release_date": "2002-05-16",
  },
  {
    "episode_nb": 3,
    "title": "Revenge of the Sith",
    "director": "George Lucas",
    "producer": "Rick McCallum",
    "release_date": "2005-05-19",
  },
  {
    "episode_nb": 4,
    "title": "A New Hope",
    "director": "George Lucas",
    "producer": "Gary Kurtz, Rick McCallum",
    "release_date": "1977-05-25",
  },
  {
    "episode_nb": 5,
    "title": "The Empire Strikes Back",
    "director": "Irvin Kershner",
    "producer": "Gary Kurtz, Rick McCallum",
    "release_date": "1980-05-17",
  },
  {
    "episode_nb": 6,
    "title": "Return of the Jedi",
    "director": "Richard Marquand",
    "producer": "Howard G. Kazanjian, George Lucas, Rick McCallum",
    "release_date": "1983-05-25",
  },
  {
    "episode_nb": 7,
    "title": "The Force Awakens",
    "director": "J. J. Abrams",
    "producer": "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
    "release_date": "2015-12-11",
  },
]


def init(request):
  try:
    conn = psycopg2.connect(
      host=settings.DATABASES['default']['HOST'],
      port=settings.DATABASES['default']['PORT'],
      database=settings.DATABASES['default']['NAME'],
      user=settings.DATABASES['default']['USER'],
      password=settings.DATABASES['default']['PASSWORD'],
    )

    with conn.cursor() as cur:
      cur.execute("""CREATE TABLE ex04_movies (
        title VARCHAR(64) NOT NULL UNIQUE,
        episode_nb INT PRIMARY KEY,
        opening_crawl TEXT,
        director VARCHAR(32) NOT NULL,
        producer VARCHAR(128) NOT NULL,
        release_date DATE NOT NULL
        );
      """)

    conn.commit()
    conn.close()
    messages.success(request, "Table ex04_movies created")

  except Exception as e:
    if conn:
      conn.close()
    messages.error(request, f"Error: {e}")
  return render(request, 'ex04/index.html', {'title': 'Init ex04_movies'})


def populate(request):
  try:
    conn = psycopg2.connect(
      host=settings.DATABASES['default']['HOST'],
      port=settings.DATABASES['default']['PORT'],
      database=settings.DATABASES['default']['NAME'],
      user=settings.DATABASES['default']['USER'],
      password=settings.DATABASES['default']['PASSWORD'],
    )

    cur = conn.cursor()

    for movie in movies:
      try:
        cur.execute("""
          INSERT INTO ex04_movies (episode_nb, title, director, producer, release_date)
          VALUES (%s, %s, %s, %s, %s)
          ON CONFLICT (episode_nb) DO UPDATE SET
          title = EXCLUDED.title,
          director = EXCLUDED.director,
          producer = EXCLUDED.producer,
          release_date = EXCLUDED.release_date
        """, (
            movie["episode_nb"],
            movie["title"],
            movie["director"],
            movie["producer"],
            movie["release_date"],
          )
        )
        conn.commit()
        messages.success(request, f"OK, Movie {movie['title']} updated")
      except Exception as e:
        messages.error(request, f"Error: {e}")
        conn.rollback()

    conn.close()

  except Exception as e:
    if conn:
      conn.close()
    messages.error(request, f"Error: {e}")
  return render(request, 'ex04/index.html', {'title': 'Populate ex04_movies'})


def display(request):
  try:
    conn = psycopg2.connect(
      host=settings.DATABASES['default']['HOST'],
      port=settings.DATABASES['default']['PORT'],
      database=settings.DATABASES['default']['NAME'],
      user=settings.DATABASES['default']['USER'],
      password=settings.DATABASES['default']['PASSWORD'],
    )

    with conn.cursor() as cur:
      cur.execute("SELECT * FROM ex04_movies")
      movies = cur.fetchall()
      if not movies:
        raise Exception("No data available")
      conn.close()
      return render(request, 'ex04/index.html', {'movies': movies, 'title': 'Display ex04_movies'})

  except Exception:
    if conn:
      conn.close()
    messages.error(request, "No data available")
    return render(request, 'ex04/index.html', {'title': 'Display ex04_movies'})


@require_http_methods(["GET", "POST"])
def remove(request):
  try:
    conn = psycopg2.connect(
      host=settings.DATABASES['default']['HOST'],
      port=settings.DATABASES['default']['PORT'],
      database=settings.DATABASES['default']['NAME'],
      user=settings.DATABASES['default']['USER'],
      password=settings.DATABASES['default']['PASSWORD'],
    )

    with conn.cursor() as cur:
      if request.method == 'POST':
        movie_to_remove = request.POST.get('movie')
        cur.execute("DELETE FROM ex04_movies WHERE title = %s", (movie_to_remove,))
        conn.commit()

      cur.execute("SELECT * FROM ex04_movies")
      movies = cur.fetchall()
      if not movies:
        raise Exception()

    return render(request, 'ex04/remove.html', {'movies': movies, 'title': 'Remove ex04_movies'})

  except Exception as e:
    if conn:
      conn.close()
    messages.error(request, "No data available")
    return render(request, 'ex04/remove.html', {'title': 'Remove ex04_movies'})