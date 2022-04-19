#!/bin/bash

sudo systemctl restart nginx
sudo systemctl restart uwsgi
sudo curl -s https://panorama-intellect.me