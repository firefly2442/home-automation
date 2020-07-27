#!/bin/bash

# prep certs, this cannot be done in the Dockerfile because
# we also need to copy them to a mounted volume
cp /usr/local/share/ca-certificates/cert.crt /config/keys/cert.crt
cp /usr/local/share/ca-certificates/cert.key /config/keys/cert.key
cp /usr/local/share/ca-certificates/ServerName /config/keys/ServerName

update-ca-certificates


/sbin/my_init