#!/bin/bash

# prep certs, this cannot be done in the Dockerfile because
# we also need to copy them to a mounted volume
cp /usr/local/share/ca-certificates/cert.crt /config/ssl/cert.crt
cp /usr/local/share/ca-certificates/cert.key /config/ssl/cert.key

update-ca-certificates

# create base64 PEM file from cert
openssl x509 -in /config/ssl/cert.crt -out /config/ssl/cert.pem

# add the pem to the certifi Python package certificate authority file
# the Python requests library does not use the system default CA, but uses the CA from the certifi package
# adding the PEM lets HA not spam warnings about insecure connections in the logs
cat /usr/local/lib/python3.8/site-packages/certifi/cacert.pem /config/ssl/cert.pem > /usr/local/lib/python3.8/site-packages/certifi/cacert-updated.pem
mv /usr/local/lib/python3.8/site-packages/certifi/cacert-updated.pem /usr/local/lib/python3.8/site-packages/certifi/cacert.pem

# blocks until zoneminder is ready to prevent race condition with HA startup
python3 /check_zoneminder.py

/init
