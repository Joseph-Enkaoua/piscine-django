python3 -m venv venv
sudo docker-compose up -d
source venv/bin/activate
pip3 install -r requirement.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 -B manage.py loaddata ex10/data/ex10_initial_data.json
python3 manage.py runserver

# source venv/bin/activate && python manage.py runserver
# docker-compose up -d
# docker exec -it sql-db-1 sh
# psql -U djangouser -d djangotraining (-h HOST -p PORT if not from container)
