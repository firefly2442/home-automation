#!/bin/bash

# https://github.com/blakeblackshear/frigate-hass-integration
# https://blakeblackshear.github.io/frigate/usage/home-assistant
cd /home/carlsonp/src/frigate-hass-integration/
git pull origin master
cp -r -f ./custom_components /media/usbdrive/homeassistant/

cd /home/carlsonp/src/home-automation/
docker compose build --pull
docker compose up -d
