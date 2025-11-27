# Eventify - Django

This repository contains a production-oriented Django project skeleton for the Eventify application.

## Features
- Custom `User` model
- EventType (categories), Event, EventImages models
- CRUD for EventType, Event, and Users
- Bootstrap-based templates and navigation
- Settings prepared to use environment variables for production

## Quick start (development)
1. Create a virtualenv and activate it
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
2. Run migrations and create superuser
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Production notes
- Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, and `DJANGO_ALLOWED_HOSTS` environment variables
- Collect static files with `python manage.py collectstatic`
- Serve via uWSGI/gunicorn + nginx or any WSGI server

