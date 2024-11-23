#! /bin/bash

#
# INSTALL DEPENDENCIES
#

python3 -m venv .venv
source .venv/bin/activate
which python
uv sync


#
# RUN MIGRATIONS AND SEED DATABASE
#

DJANGO_SUPERUSER_PASSWORD="thp.F26zeJ"
DJANGO_SUPERUSER_EMAIL="cleon@mail.info"
DJANGO_SUPERUSER_USERNAME="cleon"

./manage.py makemigrations --noinput
./manage.py migrate --noinput
./manage.py createsuperuser --user $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL --noinput
./manage.py runscript seed_database
