# https://hub.docker.com/_/eclipse-mosquitto
FROM eclipse-mosquitto:latest

RUN apk --no-cache add tzdata

USER mosquitto

COPY mosquitto.conf /mosquitto/config/mosquitto.conf

RUN chmod o+w /mosquitto/log/