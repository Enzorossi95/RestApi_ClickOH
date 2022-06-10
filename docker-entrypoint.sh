#!/bin/bash
set -e

if [ -n "$1" ]; then
    exec "$@"
fi

mkdir -p /usr/src/logs

# Prepare log files and start outputting logs to stdout
touch /usr/src/logs/gunicorn.log
touch /usr/src/logs/access.log
tail -n 0 -f /usr/src/logs/*.log &


python ../docker/web/check_db.py --service-name Postgres --ip db --port 5432

python manage.py makemigrations

python manage.py migrate
python manage.py collectstatic --noinput  # Collect static files

python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL

echo Starting Gunicorn.
if [ "$ENV" = "development" ] ; then
    (exec gunicorn --reload ClickOH_Challenge.wsgi --bind 0.0.0.0:8000)
else
    (exec gunicorn ClickOH_Challenge.wsgi \
         --name core \
         --bind 0.0.0.0:8000 \
         --workers 3 \
         --timeout 120 \
         --worker-class gevent \
         --log-level=info \
         --log-file=/usr/src/logs/gunicorn.log \
         --access-logfile=/usr/src/logs/access.log \
         "$@")
fi
