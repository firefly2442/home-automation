#!/bin/bash

./initial-setup.sh
docker-compose build
docker stop homeassistant
docker rm homeassistant
#docker run -it home-automation_homeassistant --network=home-automation_default --name=home-automation_homeassistant -v /media/usbdrive/homeassistant:/config -v /media/usbdrive/zoneminder/data:/config/www/zoneminder --device /dev/serial/by-id/usb-Silicon_Labs_HubZ_Smart_Home_Controller_C1300092-if01-port0:/dev/ttyUSB1
docker-compose up -d
