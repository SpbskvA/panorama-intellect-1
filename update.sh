#!/bin/bash

workon env
git pull
pip install -r reqirements.txt
python3 manage.py migrate --run-syncdb
python3 manage.py migrate collectstatic --noinput
