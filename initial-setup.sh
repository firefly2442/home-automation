#!/bin/bash

docker cp ./homeassistant/configuration.yaml homeassistant:/config/configuration.yaml
docker cp ./homeassistant/ui-lovelace.yaml homeassistant:/config/ui-lovelace.yaml
docker cp ./homeassistant/secrets.yaml homeassistant:/config/secrets.yaml

# add logo image for user
docker exec homeassistant mkdir -p /config/www/
docker cp ./homeassistant/binary_logo.jpg homeassistant:/config/www/binary_logo.jpg

# add config file for Zoneminder Event Server and object detection
docker cp ./zoneminder/zmeventnotification.ini zoneminder:/config/zmeventnotification.ini
docker cp ./zoneminder/secrets.ini zoneminder:/config/secrets.ini
docker cp ./zoneminder/objectconfig.ini zoneminder:/config/hook/objectconfig.ini

# download yolo3 model
# https://pjreddie.com/darknet/yolo/
if [ ! -f "./yolo/yolov3.weights" ]; then
    # 248 MB
    # md5sum: c84e5b99d0e52cd466ae710cadf6d84c
    wget https://pjreddie.com/media/files/yolov3.weights -P ./yolo/
fi