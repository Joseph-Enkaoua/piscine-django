from django.contrib import messages
from django.shortcuts import render
from django.conf import settings
from psycopg2 import sql, connect


def init(request):
  try:
    conn = connect(
      host=settings.DATABASES['default']['HOST'],
      port=settings.DATABASES['default']['PORT'],
      database=settings.DATABASES['default']['NAME'],
      user=settings.DATABASES['default']['USER'],
      password=settings.DATABASES['default']['PASSWORD'],
    )

    with conn.cursor() as cur:
      cur.execute("""CREATE TABLE IF NOT EXISTS ex08_planets (
          id SERIAL PRIMARY KEY,
          name VARCHAR(64) UNIQUE NOT NULL,
          climate TEXT,
          diameter INT,
          orbital_period INT,
          population BIGINT,
          rotation_period INT,
          surface_water REAL,
          terrain VARCHAR(128)
        );
                  
        CREATE TABLE IF NOT EXISTS ex08_people (
          id SERIAL PRIMARY KEY,
          name VARCHAR(64) UNIQUE NOT NULL,
          birth_year VARCHAR(32),
          gender VARCHAR(32),
          eye_color VARCHAR(32),
          hair_color VARCHAR(32),
          height INT,
          mass REAL,
          homeworld VARCHAR(64) REFERENCES ex08_planets(name)
        );
      """)

    conn.commit()
    conn.close()
    messages.success(request, 'OK - created ex08_planets table and ex08_people table')
    return render(request, 'ex08/display.html', {'title': 'Init Ex08'})

  except Exception as e:
    if conn:
      conn.close()
    messages.error(request, e)
    return render(request, 'ex08/display.html', {'title': 'Init Ex08'})


def populate(request):
  try:
    conn = connect(
      host=settings.DATABASES['default']['HOST'],
      port=settings.DATABASES['default']['PORT'],
      database=settings.DATABASES['default']['NAME'],
      user=settings.DATABASES['default']['USER'],
      password=settings.DATABASES['default']['PASSWORD'],
    )

    cur = conn.cursor()

    columns = ('name', 'climate', 'diameter', 'orbital_period', 'population', 'rotation_period', 'surface_water', 'terrain')
    with open("ex08/data/planets.csv", "r") as f:
      cur.copy_from(f, 'ex08_planets', sep='\t', columns=columns, null='NULL')
    conn.commit()

    messages.success(request, "OK - Planets data has been successfully imported from CSV file")

    columns = ('name', 'birth_year', 'gender', 'eye_color', 'hair_color', 'height', 'mass', 'homeworld')
    with open("ex08/data/people.csv", "r") as f:
      cur.copy_from(f, 'ex08_people', sep="\t", columns=columns, null='NULL')
    conn.commit()

    messages.success(request, "OK - People data has been successfully imported from CSV file")

    cur.close()
    conn.close()
    return render(request, 'ex08/display.html', {'title': 'Populate Ex08'})
  except Exception as e:
    if conn:
      conn.rollback()
      conn.close()
    messages.error(request, e)
    return render(request, 'ex08/display.html', {'title': 'Populate Ex08'})


def display(request):
  select_query = sql.SQL("""SELECT ex08_people.name,
                  ex08_people.homeworld,
                  ex08_planets.climate
                  FROM ex08_people JOIN ex08_planets
                  ON ex08_people.homeworld = ex08_planets.name
                  WHERE ex08_planets.climate LIKE '%windy%'
                  ORDER BY ex08_people.name""")
  try:
    conn = connect(
      host=settings.DATABASES['default']['HOST'],
      port=settings.DATABASES['default']['PORT'],
      database=settings.DATABASES['default']['NAME'],
      user=settings.DATABASES['default']['USER'],
      password=settings.DATABASES['default']['PASSWORD'],
    )

    with conn.cursor() as cur:
      cur.execute(select_query)
      people = cur.fetchall()

    conn.close()
    return render(request, 'ex08/display.html', {'people': people, 'title': 'Display Ex08'})

  except Exception:
    if conn:
      conn.close()
    messages.error(request, 'No data available')
    return render(request, 'ex08/display.html', {'title': 'Display Ex08'})
