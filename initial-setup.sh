#!/bin/bash

docker cp ./homeassistant/configuration.yaml homeassistant:/config/configuration.yaml
docker cp ./homeassistant/ui-lovelace.yaml homeassistant:/config/ui-lovelace.yaml
docker cp ./homeassistant/secrets.yaml homeassistant:/config/secrets.yaml

# add logo image for user
docker exec homeassistant mkdir -p /config/www/
docker cp ./homeassistant/binary_logo.jpg homeassistant:/config/www/binary_logo.jpg
