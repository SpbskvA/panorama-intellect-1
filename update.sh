#!/bin/bash

workon env
git pull
python3 manage.py migrate --run-syncdb
python3 manage.py migrate collectstatic --noinput
