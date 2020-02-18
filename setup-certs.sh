#!/bin/bash

# generate self-signed keys
openssl req -x509 -nodes -days 4096 -newkey rsa:2048 -out cert.crt -keyout cert.key -subj "/C=US/ST=Self/L=Self/O=Self/CN=192.168.1.113"

# copy keys to zoneminder
docker cp cert.crt zoneminder:/config/keys/cert.crt
docker cp cert.key zoneminder:/config/keys/cert.key
docker cp ServerName zoneminder:/config/keys/ServerName

docker exec homeassistant mkdir -p /config/ssl/

# copy keys to home-assistant
docker cp cert.crt homeassistant:/config/ssl/cert.crt
docker cp cert.key homeassistant:/config/ssl/cert.key

docker cp cert.crt homeassistant:/usr/local/share/ca-certificates/cert.crt
docker cp cert.crt homeassistant:/etc/ssl/certs/cert.crt

docker exec homeassistant update-ca-certificates