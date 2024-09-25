from django.contrib import messages # type: ignore
from django.shortcuts import render, redirect # type: ignore
from django.conf import settings
import psycopg2 # type: ignore

movies = [
  (1, "The Phantom Menace", "George Lucas", "Rick McCallum", "1999-05-19"),
  (2, "Attack of the Clones", "George Lucas", "Rick McCallum", "2002-05-16"),
  (3, "Revenge of the Sith", "George Lucas", "Rick McCallum", "2005-05-19"),
  (4, "A New Hope", "George Lucas", "Gary Kurtz, Rick McCallum", "1977-05-25"),
  (5, "The Empire Strikes Back", "Irvin Kershner", "Gary Kurtz, Rick McCallum", "1980-05-17"),
  (6, "Return of the Jedi", "Richard Marquand", "Howard G. Kazanjian, George Lucas, Rick McCallum", "1983-05-25"),
  (7, "The Force Awakens", "J. J. Abrams", "Kathleen Kennedy, J. J. Abrams, Bryan Burk", "2015-12-11")
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
    messages.success(request, "Table ex06_movies created")

  except Exception as e:
    if conn:
      conn.close()
    messages.error(request, str(e))
  return render(request, 'ex06/display.html', {'title': 'Init ex06'})


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
          INSERT INTO ex06_movies (episode_nb, title, director, producer, release_date)
          VALUES (%s, %s, %s, %s, %s)""", (movie[0], movie[1], movie[2], movie[3], movie[4],)
        )
        conn.commit()
        messages.success(request, f"OK - Insert {movie['title']} successful")
      except Exception as e:
        messages.error(request, f"Error - Insert {movie['title']} failed: {str(e)}")
        conn.rollback()
    conn.close()

  except Exception as e:
    if conn:
      conn.close()
    messages.error(request, str(e))
  return render(request, 'ex06/display.html', {'title': 'Populate ex06'})


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
      conn.close()
      return render(request, 'ex06/display.html', {'movies': movies, 'title': 'Display ex06'})

  except Exception:
    if conn:
      conn.close()
    messages.error(request, "No data available")
    return render(request, 'ex06/display.html', {'title': 'Display ex06'})


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
      return render(request, 'ex06/update.html', {'movies': movies, 'title': 'Update ex06'})

  except:
    if conn:
      conn.close()
    messages.error(request, "No data available")
    return render(request, 'ex06/update.html', {'title': 'Update ex06'})
