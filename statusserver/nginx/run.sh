#!/bin/sh
cp /code/nginx/nginx.conf /etc/nginx/nginx.conf
cp /code/nginx/nginx.vh.default.conf /etc/nginx/conf.d/default.conf
python /code/nginx/generateconfig.py && nginx -g "daemon off;" -c /etc/nginx/nginx.conf
