from django.contrib import messages
from django.shortcuts import render
from django.conf import settings
import psycopg2

movies = [
  (1, "The Phantom Menace", "George Lucas", "Rick McCallum", "1999-05-19"),
  (2, "Attack of the Clones", "George Lucas", "Rick McCallum", "2002-05-16"),
  (3, "Revenge of the Sith", "George Lucas", "Rick McCallum", "2005-05-19"),
  (4, "A New Hope", "George Lucas", "Gary Kurtz, Rick McCallum", "1977-05-25"),
  (5, "The Empire Strikes Back", "Irvin Kershner", "Gary Kurtz, Rick McCallum", "1980-05-17"),
  (6, "Return of the Jedi", "Richard Marquand", "Howard G. Kazanjian, George Lucas, Rick McCallum", "1983-05-25"),
  (7, "The Force Awakens", "J. J. Abrams", "Kathleen Kennedy, J. J. Abrams, Bryan Burk", "2015-12-11"),
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
      cur.execute("""CREATE TABLE ex02_movies (
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
    messages.success(request, "OK, Table ex02_movies created successfully")

  except Exception as e:
    if conn:
      conn.close()
    messages.error(request, f"KO {str(e)}")
  return render(request, 'ex02/display.html', {'title': 'Init ex02_movies'})
  

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
          INSERT INTO ex02_movies (episode_nb, title, director, producer, release_date)
          VALUES (%s, %s, %s, %s, %s)""", (movie[0], movie[1], movie[2], movie[3], movie[4])
        )
        conn.commit()
        messages.success(request, f"OK, {movie['title']} added successfully")
      except Exception as e:
        messages.error(request, f"KO {str(e)}")
        conn.rollback()

    conn.close()

  except Exception as e:
    if conn:
      conn.close()
    messages.error(request, f"KO {str(e)}")
  return render(request, 'ex02/display.html', {'title': 'Populate ex02_movies'})


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
      return render(request, 'ex02/display.html', {'movies': movies, 'title': 'Display ex02_movies'})

  except Exception as e:
    if conn:
      conn.close()
    messages.error(request, f"KO {str(e)}")
    return render(request, 'ex02/display.html', {'title': 'Display ex02_movies'})
  