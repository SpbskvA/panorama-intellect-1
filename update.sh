#!/bin/bash

workon env
git pull
pip install -r requirements.txt
python3 manage.py migrate --run-syncdb
python3 manage.py collectstatic --noinput
