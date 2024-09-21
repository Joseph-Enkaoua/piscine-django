from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
import psycopg2

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
      cur.execute("""CREATE TABLE IF NOT EXISTS ex02_movies (
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
    return HttpResponse("OK")

  except Exception as e:
    if conn:
      conn.close()
    return HttpResponse(e)
  

def populate(request):
  try:
    conn = psycopg2.connect(
      host=settings.DATABASES['default']['HOST'],
      port=settings.DATABASES['default']['PORT'],
      database=settings.DATABASES['default']['NAME'],
      user=settings.DATABASES['default']['USER'],
      password=settings.DATABASES['default']['PASSWORD'],
    )

    movies = [
      {
        "episode_nb": 1,
        "title": "The Phantom Menace",
        "director": "George Lucas",
        "producer": "Rick McCallum",
        "elease_date": "1999-05-19",
      },
      {
        "episode_nb": 2,
        "title": "Attack of the Clones",
        "director": "George Lucas",
        "producer": "Rick McCallum",
        "elease_date": "2002-05-16",
      },
      {
        "episode_nb": 3,
        "title": "Revenge of the Sith",
        "director": "George Lucas",
        "producer": "Rick McCallum",
        "elease_date": "2005-05-19",
      },
      {
        "episode_nb": 4,
        "title": "A New Hope",
        "director": "George Lucas",
        "producer": "Gary Kurtz, Rick McCallum",
        "elease_date": "1977-05-25",
      },
      {
        "episode_nb": 5,
        "title": "The Empire Strikes Back",
        "director": "Irvin Kershner",
        "producer": "Gary Kurtz, Rick McCallum",
        "elease_date": "1980-05-17",
      },
      {
        "episode_nb": 6,
        "title": "Return of the Jedi",
        "director": "Richard Marquand",
        "producer": "Howard G. Kazanjian, George Lucas, Rick McCallum",
        "elease_date": "1983-05-25",
      },
      {
        "episode_nb": 7,
        "title": "The Force Awakens",
        "director": "J. J. Abrams",
        "producer": "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
        "elease_date": "2015-12-11",
      },
    ]

    results = []

    cur = conn.cursor()

    for movie in movies:
      try:
        cur.execute("""
          INSERT INTO ex02_movies (episode_nb, title, director, producer, release_date)
          VALUES (%s, %s, %s, %s, %s)""", (
            movie["episode_nb"],
            movie["title"],
            movie["director"],
            movie["producer"],
            movie["elease_date"],
          )
        )
        conn.commit()
        results.append("OK")
      except Exception as e:
        results.append(str(e))
        conn.rollback()

    conn.close()
    return HttpResponse("<br/>".join(str(i) for i in results))

  except Exception as e:
    if conn:
      conn.close()
    return HttpResponse(e)


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
      cur.execute("SELECT * FROM ex02_movies")
      movies = cur.fetchall()
      conn.close()
      return render(request, 'ex02/display.html', {'movies': movies})

  except Exception as e:
    if conn:
      conn.close()
    return HttpResponse(e)
  