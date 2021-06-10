#!/bin/bash

cp -f ../.env .

docker-compose up -d --build
