#!/bin/bash

#docker run -d -p 8082:80 --mount type=bind,source="$(pwd)",target=/var/www/html php:apache
#docker run -p 8080:80 --mount type=bind,source="$(pwd)",target=/var/www/html php:apache
php -S 0.0.0.0:8080

