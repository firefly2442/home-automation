#!/bin/bash

docker-compose build
docker rm yolo
docker run -it --network=home-automation_default --name=yolo -v /media/usbdrive/zoneminder/data:/var/cache/zoneminder -v /yolo

