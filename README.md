# Home Automation

My personal home automation setup in Docker leveraging:

* [Zoneminder](https://github.com/ZoneMinder/zoneminder)
* [Home-Assistant](https://github.com/home-assistant/home-assistant)
* [OpenWRT](https://openwrt.org/)

## Setup

Install Docker and run Linux post-install steps so you don't need `sudo` for your regular user.

Install docker-compose.

Install the proprietary Nvidia drivers via the "Additional Drivers" GUI.

Follow directions for [installing nvidia-docker](https://github.com/NVIDIA/nvidia-docker) support

Use `sudo watch -n0.5 nvidia-smi` to check things are working

Use `sudo nvtop` for a graphical view of the GPU usage

Until [docker-compose](https://github.com/docker/compose/issues/6691) support works, GPU support is hacky.

Check to make sure [Tensorflow via GPUs](https://www.tensorflow.org/install/docker) works by following instructions
for testing by running a Docker image to calculate a tensor.

```shell
# attempt to circumvent docker-compose GPU inability, join the Docker network that docker-compose creates
docker-compose build
docker stop yolo
docker rm yolo
docker run --gpus all -it --network=home-automation_default --name=yolo -v /backup2/zoneminder/data:/var/cache/zoneminder -v /yolo -v /backup2/yolo/:/testing home-automation_yolo
```

Copy `.env-copy` to `.env` and edit

Copy `homeassistant/secrets_copy.yaml` to `homeassistant/secrets.yaml` and edit

Copy `zoneminder/secrets_copy.ini` to `zoneminder/secrets.ini` and edit

```shell
docker-compose up --build -d
```

Wait until `zoneminder` is up and running.  This will take some time, you can check the progress via:

```shell
docker logs -f zoneminder
```

Run `setup-certs.sh`

Run `initial-setup.sh`

Run `setup-options.sh`

Run `setup-cameras.sh`

Restart `zoneminder`:

```shell
docker restart zoneminder
```

There's an annoying race condition where homeassistant doesn't get setup correctly
if zoneminder isn't running.

```shell
docker restart homeassistant
```

Install the [home-assistant Android application](https://play.google.com/store/apps/details?id=io.homeassistant.companion.android&hl=en_US)
on cellphone

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

Inside Camera (Samsung Galaxy Nexus cellphone)

* Uses the [IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en_US)
application for Android
* `http://admin:secret@192.168.1.116:8080/video`
* 1280 x 720 (30 fps)
* x264 encoding

### Additional Setup

* Review [filters](https://zoneminder.readthedocs.io/en/latest/userguide/filterevents.html) for purging
disk when full, reduce deletion from 100 to 10 events

### Event Server for Object Detection

See `zoneminder/*.ini` files

There's also [extensive documentation](https://zmeventnotification.readthedocs.io/en/stable/guides/hooks.html)
on the hooks system, object detection methods/libraries, configuration, and more.

## Home Assistant

Upon startup, register with name `Patrick` and username `patrick`.

See `configuration.yaml` for devices and setup

See `ui-lovelace.yaml` for UI configuration

### Updating UI

Make changes, then run `initial-setup.sh` to copy the `ui-lovelace.yaml` file over,
then refresh the page.

### Smart Power Plug Switches

TP-Link HS105 smart switches.  Uses the `Kasa` Android app for setup.

## Yolo object detection

Run `yolo.py`

### Benchmarking and Profiling Performance

```shell
python3 -m pyinstrument yolo.py
```

## Networking

Setup Network -> Firewall rules in OpenWRT to reject any packages from the LAN
to WAN.  This allows it on the local network
but disallows all Internet traffic.  This way you can block things like the
cellphone, smart plugs, etc.

## Updates

If there are updates upstream in the Docker images:

```shell
docker-compose build --pull
# or force a full rebuild
# docker-compose build --no-cache --pull
docker-compose up -d
```

## Teardown

```shell
docker-compose down -v
```

Cleanup files from the mounted Docker volumes

## Helpful Links and References

* [Zoneminder and HA integration with zmEventServer](https://seanb.co.uk/2019/08/zoneminder-and-home-assistant/)
* [Managing notifications in HA](https://seanb.co.uk/2019/08/managing-zoneminder-notifications-with-home-assistant/)
* [Dockerized version of Zoneminder](https://github.com/dlandon/zoneminder)
* [zmeventnotification for object detection](https://github.com/pliablepixels/zmeventnotification)

## TODO

* upload image / email alert on identifying person
* zoneminder person detection
* alarm on person detected
* flash lights when person detected
* randomly turn on/off lights when away
* cleanup device tracker listing
* add health check for Docker containers
* fix weather, noise option?
* cleanup old event server configs and references
* rebuild zoneminder w/out event server
