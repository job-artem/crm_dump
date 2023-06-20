#!/bin/bash

python manage.py migrate --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py loaddata data/time_data.json
python manage.py loaddata data/location.json
python manage.py loaddata data/section.json
python manage.py loaddata data/days.json
python manage.py loaddata data/age.json
python manage.py loaddata data/groups_type.json
python manage.py collectstatic --noinput
gunicorn --config project/settings/gunicorn_config.py project.network.wsgi:application --reload --preload
