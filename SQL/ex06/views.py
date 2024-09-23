from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
import psycopg2

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
      cur.execute("""CREATE TABLE IF NOT EXISTS ex06_movies (
          title VARCHAR(64) NOT NULL UNIQUE,
          episode_nb INT PRIMARY KEY,
          opening_crawl TEXT,
          director VARCHAR(32) NOT NULL,
          producer VARCHAR(128) NOT NULL,
          release_date DATE NOT NULL,
          created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
                
        CREATE OR REPLACE FUNCTION update_changetimestamp_column()
        RETURNS TRIGGER AS $$
        BEGIN
        NEW.updated = now();
        NEW.created = OLD.created;
        RETURN NEW;
        END;
        $$ language 'plpgsql';
        CREATE TRIGGER update_films_changetimestamp BEFORE UPDATE
        ON ex06_movies FOR EACH ROW EXECUTE PROCEDURE
        update_changetimestamp_column();
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


    results = []

    cur = conn.cursor()

    for movie in movies:
      try:
        cur.execute("""
          INSERT INTO ex06_movies (episode_nb, title, director, producer, release_date)
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
      cur.execute("SELECT * FROM ex06_movies ORDER BY episode_nb")
      movies = cur.fetchall()
      if not movies:
        raise Exception("No data available")
      conn.close()
      return render(request, 'ex06/display.html', {'movies': movies})

  except Exception:
    if conn:
      conn.close()
    return HttpResponse("No data available")


def update(request):
  try:
    conn = psycopg2.connect(
      host=settings.DATABASES['default']['HOST'],
      port=settings.DATABASES['default']['PORT'],
      database=settings.DATABASES['default']['NAME'],
      user=settings.DATABASES['default']['USER'],
      password=settings.DATABASES['default']['PASSWORD'],
    )

    with conn.cursor() as cur:
      cur.execute("SELECT * FROM ex06_movies")
      movies = cur.fetchall()
      if not movies:
        raise Exception("No data available")

      if request.method == 'POST':
        movie_to_update = request.POST.get('movie')
        opening_crawl = request.POST.get('opening_crawl')
        if opening_crawl:
          cur.execute("""
            UPDATE ex06_movies
            SET opening_crawl = %s
            WHERE title = %s
          """, (opening_crawl, movie_to_update))
          conn.commit()
          conn.close()
          return redirect('/ex06/display')

      conn.close()
      return render(request, 'ex06/update.html', {'movies': movies})

  except:
    if conn:
      conn.close()
    return HttpResponse("No data available")
