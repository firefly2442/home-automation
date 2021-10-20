# Home Automation

[![Total alerts](https://img.shields.io/lgtm/alerts/g/firefly2442/home-automation.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/firefly2442/home-automation/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/firefly2442/home-automation.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/firefly2442/home-automation/context:python)

My personal home automation setup in Docker leveraging:

* [Zoneminder](https://github.com/ZoneMinder/zoneminder)
* [Home-Assistant](https://github.com/home-assistant/home-assistant)

## Setup

Install Docker and run Linux post-install steps so you don't need `sudo` for your regular user.

Install docker-compose.

Copy `.env-copy` to `.env` and edit

Copy `homeassistant/secrets_copy.yaml` to `homeassistant/secrets.yaml` and edit

Copy `flaskcamera/config.example.py` to `flaskcamera/config.py` and edit

Run `setup-certs.sh`

Build our docker-compose and bring up services

```shell
docker-compose up --build -d
```

Wait until `zoneminder` is up and running.  This will take some time, you can check the progress via:

```shell
docker logs -f zoneminder
```

Run `initial-setup.sh`

Run `setup-options.sh`

Run `setup-cameras.sh`

Restart `zoneminder`:

```shell
docker restart zoneminder
```

Install the [home-assistant Android application](https://play.google.com/store/apps/details?id=io.homeassistant.companion.android&hl=en_US)
on cellphone

Setup Frigate on Raspberry Pi 3 B+.  Set `FRIGATE_RTSP_PASSWORD` in `.env` which is the camera password.  See `frigate` folder.  Run `run-frigate.sh`.

Leverages the [integration with HA](https://blakeblackshear.github.io/frigate/usage/home-assistant)
Script copies `custom_components` folder over to `/media/usbdrive/homeassistant/` as part of home automation
refresh and update process.

Use the `run-home-automation.sh` for future changes and to grab the latest versions of Docker images.

## UI

* [Zoneminder - https://192.168.1.226:9443/zm/](https://192.168.1.226:9443/zm/)
* [Home-Assistant - http://192.168.1.226:8123](http://192.168.1.226:8123)
* [ZWaveJS - http://192.168.1.226:8091](http://192.168.1.226:8091/)

## Zoneminder

### Cameras

Don't use h265, zoneminder and frigate struggle with this.

Camera (Amcrest IP4M-1051W - 4MP)

* Web-UI: `http://192.168.1.111`
* `rtsp://admin:secret@192.168.1.111:554/cam/realmonitor?channel=1&subtype=0`
* 2688 x 1520 (20 fps)
* h264 passthrough

Camera (Amcrest IP8M-2493EW - 8MP - x2)

* Web-UI: `http://192.168.1.110`, `http://192.168.1.112`
* `rtsp://admin:secret@192.168.1.110:554/cam/realmonitor?channel=1&subtype=0`
* 3840 x 2160 (15 fps)
* h264 passthrough

Camera (Samsung Galaxy Nexus cellphone)

* Uses the [IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en_US)
application for Android
* `rtsp://admin:secret@192.168.1.116:8080/h264_pcm.sdp`
* 1280 x 720 (30 fps)
* h264 passthrough

### Additional Setup

* Review [filters](https://zoneminder.readthedocs.io/en/latest/userguide/filterevents.html) for purging
disk when full, reduce deletion from 100 to 10 events

## Home Assistant

Upon startup, register with name `Patrick` and username `patrick`.

See `configuration.yaml` for devices and setup

See `ui-lovelace.yaml` for UI configuration

### Updating UI

Make changes, then run `initial-setup.sh` to copy the `ui-lovelace.yaml` file over,
then refresh the page.

### Smart Power Plug Switches

TP-Link HS105 smart switches with various hardware versions.  Uses the `Kasa` Android app for setup.

## Networking

Setup Network -> Firewall rules in OpenWRT to reject any packages from the LAN
to WAN.  This allows it on the local network
but disallows all Internet traffic.  This way you can block things like the
cellphone, smart plugs, etc.

## Updates

If there are updates upstream in the Docker images:

```shell
docker-compose build --pull --parallel
# or force a full rebuild
# docker-compose build --no-cache --pull --parallel
docker-compose up -d
```

## Teardown

```shell
docker-compose down -v
```

Cleanup files from the mounted Docker volumes

## TODO

* check pihole status and notify if down
* setup two new cameras
* add zwavejs version to update check
* turn on alarm after sufficient testing
* get dimmer switch working, zwave
* flash lights when person detected
* make sure scaled images and event folders get cleared away by zoneminder filter deletion
* add explanatory text on containers, documentation, images/GIFs to README, add helpful links
