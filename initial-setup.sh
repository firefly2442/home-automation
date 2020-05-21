#!/bin/bash

docker cp ./homeassistant/configuration.yaml homeassistant:/config/configuration.yaml
docker cp ./homeassistant/ui-lovelace.yaml homeassistant:/config/ui-lovelace.yaml

# add logo image for user
docker exec homeassistant mkdir -p /config/www/
docker cp ./homeassistant/binary_logo.jpg homeassistant:/config/www/binary_logo.jpg

# download yolo3 pretrained model
# https://pjreddie.com/darknet/yolo/
if [ ! -f "./yolo/yolov3.weights" ]; then
    # 248 MB
    # md5sum: c84e5b99d0e52cd466ae710cadf6d84c
    wget -nc https://pjreddie.com/media/files/yolov3.weights -P ./yolo/
fi

# download yolo3-tiny pretrained model
# https://pjreddie.com/darknet/yolo/
if [ ! -f "./yolo/yolov3-tiny.weights" ]; then
    # 34 MB
    # md5sum: 3bcd6b390912c18924b46b26a9e7ff53
    wget -nc https://pjreddie.com/media/files/yolov3-tiny.weights -P ./yolo/
fi
