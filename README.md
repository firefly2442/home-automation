# Home Automation

[![Total alerts](https://img.shields.io/lgtm/alerts/g/firefly2442/home-automation.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/firefly2442/home-automation/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/firefly2442/home-automation.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/firefly2442/home-automation/context:python)

My personal home automation setup in Docker leveraging:

* [Frigate](https://github.com/blakeblackshear/frigate)
* [Home-Assistant](https://github.com/home-assistant/home-assistant)

## Setup

Install Docker and run Linux post-install steps so you don't need `sudo` for your regular user.

Install [Docker Compose](https://docs.docker.com/compose/).

Copy `.env-copy` to `.env` and edit

Copy `homeassistant/secrets_copy.yaml` to `homeassistant/secrets.yaml` and edit

Run `setup-certs.sh`

Build via compose and bring up services

```shell
docker compose up --build -d
```

Run `initial-setup.sh`

Install the [home-assistant Android application](https://play.google.com/store/apps/details?id=io.homeassistant.companion.android&hl=en_US)
on cellphone

Setup Frigate on main Asus computer with Nvidia decoding of h264 video.  Install Nvidia proprietary drivers
and the `nvidia-docker2` package, see [details here](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker).
Use the `nvidia-smi` command to make sure you can launch Docker and pass the GPU through properly.
Set `FRIGATE_RTSP_PASSWORD` in `.env` which is the camera password.  See `frigate` folder.  Run `run-frigate.sh`.

TODO: fix path
Leverages the [integration with HA](https://blakeblackshear.github.io/frigate/usage/home-assistant)
Script copies `custom_components` folder over to `/media/usbdrive/homeassistant/` as part of home automation
refresh and update process.  Go into integrations in Home Assistant if Frigate doesn't load properly and add it.

Use the `run-home-automation.sh` for future changes and to grab the latest versions of Docker images.

## UI

* [Frigate - https://192.168.1.113:5000](https://192.168.1.113:5000)
* [Home-Assistant - http://192.168.1.226:8123](http://192.168.1.226:8123)
* [ZWaveJS - http://192.168.1.226:8091](http://192.168.1.226:8091/)

## Zoneminder

### Cameras

Don't use h265, Frigate may struggle with this and it's not supported to replay in some browsers.

Camera (Amcrest IP4M-1051W - 4MP)

* Web-UI:
  * `http://192.168.1.111`
  * inside camera
* main stream (recording)
  * `rtsp://admin:secret@192.168.1.111:554/cam/realmonitor?channel=1&subtype=0`
  * 2688 x 1520 (20 fps)
* sub-stream (person detection)
  * `rtsp://admin:secret@192.168.1.111:554/cam/realmonitor?channel=1&subtype=1`
  * 640 x 480 (5 fps)
* h264 passthrough

Camera (Amcrest IP8M-2493EW-V2 - 8MP - x2)

* Web-UI:
  * `http://192.168.1.110`
    * frontdoor camera
  * `http://192.168.1.112`
    * backdoor camera
* main stream (recording)
  * `rtsp://admin:secret@192.168.1.110:554/cam/realmonitor?channel=1&subtype=0`
  * 3840 x 2160 (15 fps)
* sub-stream (person detection)
  * `rtsp://admin:secret@192.168.1.110:554/cam/realmonitor?channel=1&subtype=1`
  * 704 x 480 (5 fps)
* h264 passthrough

Camera (Samsung Galaxy Nexus cellphone)

* Uses the [IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en_US)
application for Android
* `rtsp://admin:secret@192.168.1.116:8080/h264_pcm.sdp`
* 1280 x 720 (30 fps)
* h264 passthrough

### Additional Setup

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
docker compose build --pull --parallel
# or force a full rebuild
# docker compose build --no-cache --pull --parallel
docker compose up -d
```

## Teardown

```shell
docker compose down -v
```

Cleanup files from the mounted Docker volumes

## TODO

* check pihole status and notify if down
* add zwavejs version to update check
* turn on alarm after sufficient testing
* get dimmer switch working, zwave
* flash lights when person detected
* check disk usage by Frigate
* add explanatory text on containers, documentation, images/GIFs to README, add helpful links
* setup Frigate with SSL certs
* fix run-home-automation.sh frigate copy location
