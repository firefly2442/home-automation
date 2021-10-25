#!/bin/bash

# if the file doesn't exist
if [ ! -f "cert.crt" ]; then
    # generate self-signed keys
    # https://security.stackexchange.com/questions/74345/provide-subjectaltname-to-openssl-directly-on-the-command-line
    # requires openssl version 1.1.1
    openssl req -x509 -nodes -days 4096 -newkey rsa:2048 -out cert.crt -keyout cert.key -subj "/C=US/ST=Self/L=Self/O=Self/CN=192.168.1.226" -addext "subjectAltName = IP:192.168.1.226"
fi

# copy key to home-assistant folder
cp cert.crt ./homeassistant/cert.crt
cp cert.key ./homeassistant/cert.key

# copy key to yolo folder
cp cert.crt ./yolo/cert.crt
cp cert.key ./yolo/cert.key
