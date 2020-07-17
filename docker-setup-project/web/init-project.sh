#!/bin/sh
rm -f -r /usr/celery
mkdir /usr/celery
python3.8 ./docker-setup-project/web/dbsetup.py

cd tatartwin && celery -A tatartwin worker -D -l info -f ../celeryd.log --pidfile /usr/celery/celeryd.pid && cd ..
cd tatartwin && celery -A tatartwin beat --detach -l info -f ../celerybeat.log --pidfile /usr/celery/celerybeat.pid && cd ..
#python3.8 ./tatartwin/manage.py runserver 0.0.0.0:8000
cd tatartwin && daphne -b 0.0.0.0 -p 8000 tatartwin.asgi:application

exec "$@"