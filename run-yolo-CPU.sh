#!/bin/bash

docker-compose build
docker rm yolo
docker run -it --network=home-automation_default --name=yolo -v /backup2/zoneminder/data:/var/cache/zoneminder -v /yolo -v /backup2/yolo/:/testing home-automation_yolo

