# Home Automation

My personal home automation setup in Docker leveraging:

* [Zoneminder](https://github.com/ZoneMinder/zoneminder)
* [Home-Assistant](https://github.com/home-assistant/home-assistant)

## Setup

Copy `.env-copy` to `.env` and edit

Copy `homeassistant/secrets_copy.yaml` to `homeassistant/secrets.yaml` and edit

```shell
docker-compose up --build -d
```

Run `setup-certs.sh`

Run `initial-setup.sh`

There's an annoying race condition where zoneminder doesn't get setup correctly.

```shell
docker restart homeassistant
```

Run `setup-cameras.sh`

Install the home-assistant Android application on cellphone

## UI

* [Zoneminder - https://192.168.1.113:8443/zm/](https://192.168.1.113:8443/zm/)
* [Home-Assistant - http://192.168.1.113:8123](http://192.168.1.113:8123)

## Zoneminder

### Cameras

Front Camera (Amcrest IP4M-1051W - 4MP)

* Web-UI: `http://192.168.1.111`
* `rtsp://admin:secret@192.168.1.111:554/cam/realmonitor?channel=1&subtype=0`
* 2688 x 1520 (20 fps)
* h264 passthrough

Cellphone (Samsung Galaxy Nexus)

* `http://admin:secret@192.168.1.116:8080/video`
* 1280 x 720 (30 fps)
* x264 encoding

### Additional Setup

* Set the timezone in options, otherwise you get warnings in the logs
* Change the refresh frequency for the UI
* Manually setup zones and tweak sensitivities for motion detection
* Review filters for purging disk when full

## Home Assistant

Upon startup, register user with `Patrick` and `carlsonp`.

Install package on OpenWRT router:

```shell
opkg update
opkg install luci-mod-rpc
```

See `configuration.yaml` for devices and setup

See `ui-lovelace.yaml` for UI configuration

### Updating UI

Make changes, then run `initial-setup.sh` to copy the `ui-lovelace.yaml` file over,
then refresh the page.

## Updates

If there are updates upstream in the Docker images:

```shell
docker-compose build --pull
docker-compose up -d
```

## Teardown

```shell
docker-compose down -v
```



TODO:

zoneminder person detection, ML
alarm on person detected
z-wave motion detection sensors?