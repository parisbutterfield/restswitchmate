#!/bin/sh
python /code/nginx/generateconfig.py && nginx -g "daemon off;" -c /etc/nginx/nginx.conf
