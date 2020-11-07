#!/bin/bash

# this is all temporary until docker-compose works properly with GPUs
docker-compose build
docker rm yolo
docker run --gpus all -it --network=home-automation_default --name=yolo -v /media/usbdrive/zoneminder/data:/var/cache/zoneminder -v /yolo

