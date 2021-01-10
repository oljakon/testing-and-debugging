#!/bin/bash
python manage.py runserver 127.0.0.1:8000
python manage.py runserver 127.0.0.1:8001 --settings=backend.settings_read_only
python manage.py runserver 127.0.0.1:8002 --settings=backend.settings_read_only
gunicorn --bind unix:/tmp/pgadmin4.sock --workers=1 --threads=25 --chdir /Applications/"pgAdmin 4.app"/Contents/Resources pgAdmin4:app