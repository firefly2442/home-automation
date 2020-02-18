#!/bin/bash

# load values from .env file
if [ -f .env ]
then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi

# load up working cameras, then load up https://192.168.1.113:8443/zm/api/monitors.json to see the correct values
# make sure to encode special characters like &'s which become %26
# https://zoneminder.readthedocs.io/en/1.34.2/api.html#add-a-monitor
curl --insecure -X POST https://192.168.1.113:8443/zm/api/monitors.json -d "Monitor[Name]=FrontCamera\
&Monitor[Function]=Mocord\
&Monitor[Type]=Ffmpeg\
&Monitor[Method]=rtpRtsp\
&Monitor[Path]=rtsp://admin:$CAMERA_PASSWORD@192.168.1.111:554/cam/realmonitor?channel=1%26subtype=0\
&Monitor[V4LCapturesPerFrame]=1\
&Monitor[RTSPDescribe]=false\
&Monitor[Width]=2688\
&Monitor[Height]=1520\
&Monitor[Colours]=4\
&Monitor[SaveJPEGs]=0\
&Monitor[VideoWriter]=2\
&Monitor[ImageBufferCount]=80\
&Monitor[WarmupCount]=0\
&Monitor[PreEventCount]=20\
&Monitor[PostEventCount]=20\
&Monitor[StreamReplayBuffer]=0\
&Monitor[LabelFormat]=\
&Monitor[AlarmFrameCount]=1"

curl --insecure -X POST https://192.168.1.113:8443/zm/api/monitors.json -d "Monitor[Name]=SideCamera\
&Monitor[Function]=Mocord\
&Monitor[Type]=Ffmpeg\
&Monitor[Method]=rtpRtsp\
&Monitor[Path]=http://admin:$CAMERA_PASSWORD@192.168.1.116:8080/video\
&Monitor[V4LCapturesPerFrame]=1\
&Monitor[RTSPDescribe]=false\
&Monitor[Width]=1280\
&Monitor[Height]=720\
&Monitor[Colours]=4\
&Monitor[SaveJPEGs]=0\
&Monitor[VideoWriter]=1\
&Monitor[ImageBufferCount]=30\
&Monitor[WarmupCount]=0\
&Monitor[PreEventCount]=5\
&Monitor[PostEventCount]=5\
&Monitor[StreamReplayBuffer]=0\
&Monitor[LabelFormat]=\
&Monitor[AlarmFrameCount]=1"