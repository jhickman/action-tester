#!/bin/bash


docker run \
    -d \
    --name 'actions-test-db' \
    --expose 5432 \
    -p '5432:5432' \
    -e POSTGRES_DB=actiontest \
    -e POSTGRES_PASSWORD=pass1234 \
    -e POSTGRES_USER=the_user \
    postgis/postgis:15-master

