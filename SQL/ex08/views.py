from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
import psycopg2


def get_name(line):
  name = ""
  for word in line.split():
    if word[0].isupper() and word != "NULL":
      name += word + " "
    else:
      break
  return name.strip()

def get_person_name(line):
  name = ""
  for word in line.split():
    if word[0].isalpha() and word != "NULL":
      name += word + " "
    else:
      break
  return name.strip()

def is_int(s):
  try:
    int(s)
    return True
  except ValueError:
    return False

def get_climate(line):
  climate = ""
  for word in line.split():
    if climate == "NULL " or is_int(word) or (climate and word == "NULL"):
      break
    climate += word + " "
  return climate.strip()

def is_not_none(s):
  return s != "NULL" and s != "none" and s != "n/a"

def parse_planets():
  planets = []
  with open("ex08/planets.csv", "r") as f:
    for line in f.readlines():
      name = get_name(line)
      line = line.replace(name, "")

      climate = get_climate(line)
      line = line.replace(climate, "", 1)

      diameter = line.split()[0]
      line = line.replace(diameter, "", 1)
      
      orbital_period = line.split()[0]
      line = line.replace(orbital_period, "", 1)

      population = line.split()[0]
      line = line.replace(population, "", 1)

      rotation_period = line.split()[0]
      line = line.replace(rotation_period, "", 1)

      surface_water = line.split()[0]
      line = line.replace(surface_water, "", 1)

      terrain = line.strip()

      planet = {
        "name": name,
        "climate": climate if is_not_none(climate) else None,
        "diameter": int(diameter) if is_not_none(diameter) else None,
        "orbital_period": int(orbital_period) if is_not_none(orbital_period) else None,
        "population": int(population) if is_not_none(population) else None,
        "rotation_period": int(rotation_period) if is_not_none(rotation_period) else None,
        "surface_water": float(surface_water) if is_not_none(surface_water) else None,
        "terrain": terrain if is_not_none(terrain) else None,
      }
      planets.append(planet)
  return planets

def parse_people():
  people = []
  with open("ex08/people.csv", "r") as f:
    for line in f.readlines():
      name = get_person_name(line)
      line = line.replace(name, "")

      birth_year = line.split()[0]
      line = line.replace(birth_year, "", 1)

      gender = line.split()[0]
      line = line.replace(gender, "", 1)

      eye_color = line.split()[0]
      line = line.replace(eye_color, "", 1)

      if eye_color[-1] == ",":
        eye_color += " " + line.split()[0]
        line = line.replace(line.split()[0], "", 1)

      hair_color = line.split()[0]
      line = line.replace(hair_color, "", 1)

      if hair_color[-1] == ",":
        hair_color += " " + line.split()[0]
        line = line.replace(line.split()[0], "", 1)

      height = line.split()[0]
      line = line.replace(height, "", 1)

      mass = line.split()[0]
      line = line.replace(mass, "", 1)

      homeworld = line.strip()

      person = {
        "name": name,
        "birth_year": birth_year if is_not_none(birth_year) else None,
        "gender": gender if is_not_none(gender) else None,
        "eye_color": eye_color if is_not_none(eye_color) else None,
        "hair_color": hair_color if is_not_none(hair_color) else None,
        "height": int(height) if is_not_none(height) else None,
        "mass": float(mass) if is_not_none(mass) else None,
        "homeworld": homeworld if is_not_none(homeworld) else None,
      }
      people.append(person)
    return people

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

    planets = parse_planets()
    people = parse_people()

    cur = conn.cursor()

    for planet in planets:
      try:
        cur.execute(
          """INSERT INTO ex08_planets (name, climate, diameter, orbital_period, population, rotation_period, surface_water, terrain) VALUES 
          (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (name) DO NOTHING""",
          (planet["name"], planet["climate"], planet["diameter"], planet["orbital_period"], planet["population"],
           planet["rotation_period"], planet["surface_water"], planet["terrain"])
        )
        conn.commit()
        results.append("OK")
      except Exception as e:
        results.append(str(e))
        conn.rollback()

    for person in people:
      try:
        cur.execute(
          """INSERT INTO ex08_people (name, birth_year, gender, eye_color, hair_color, height, mass, homeworld) VALUES
          (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (name) DO NOTHING""",
          (person["name"], person["birth_year"], person["gender"], person["eye_color"], person["hair_color"],
           person["height"], person["mass"], person["homeworld"])
        )
        conn.commit()
        results.append("OK")
      except Exception as e:
        results.append(str(e))
        conn.rollback()

    cur.close()
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
      cur.execute("""SELECT ex08_people.name,
                  ex08_people.homeworld,
                  ex08_planets.climate
                  FROM ex08_people JOIN ex08_planets
                  ON ex08_people.homeworld = ex08_planets.name
                  ORDER BY ex08_people.name""")
      people = cur.fetchall()

    conn.close()
    return render(request, "ex08/display.html", {"people": people})
  
  except Exception:
    if conn:
      conn.close()
    return HttpResponse("No data available")
