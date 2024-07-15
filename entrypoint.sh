#!/bin/sh


# Exit on error
set -e

# Run database migrations
echo "Applying database migrations"
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "Collecting static files"
python manage.py collectstatic --noinput

# Populate database
python manage.py read_data --save_category
python manage.py read_data --save_idea
python manage.py populate_db


# Start Gunicorn server
exec "$@"

