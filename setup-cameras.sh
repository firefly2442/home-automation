#!/bin/bash

# load values from .env file
if [ -f .env ]
then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi

# load up working cameras, then load up https://192.168.1.226:9443/zm/api/monitors.json to see the correct values
# make sure to encode special characters like &'s which become %26
# https://zoneminder.readthedocs.io/en/latest/api.html#add-a-monitor
curl --insecure -X POST https://192.168.1.226:9443/zm/api/monitors.json -d "Monitor[Name]=AmcrestCamera\
&Monitor[Function]=Record\
&Monitor[Type]=Ffmpeg\
&Monitor[Method]=rtpRtsp\
&Monitor[Path]=rtsp://admin:$CAMERA_PASSWORD@192.168.1.111:554/cam/realmonitor?channel=1%26subtype=0\
&Monitor[V4LCapturesPerFrame]=1\
&Monitor[RTSPDescribe]=false\
&Monitor[Width]=2688\
&Monitor[Height]=1520\
&Monitor[Colours]=4\
&Monitor[SaveJPEGs]=1\
&Monitor[VideoWriter]=2\
&Monitor[ImageBufferCount]=80\
&Monitor[WarmupCount]=0\
&Monitor[PreEventCount]=20\
&Monitor[PostEventCount]=20\
&Monitor[StreamReplayBuffer]=0\
&Monitor[LabelFormat]=\
&Monitor[AlarmFrameCount]=1"

curl --insecure -X POST https://192.168.1.226:9443/zm/api/monitors.json -d "Monitor[Name]=CellphoneCamera\
&Monitor[Function]=Record\
&Monitor[Type]=Ffmpeg\
&Monitor[Method]=rtpRtsp\
&Monitor[Path]=rtsp://admin:$CAMERA_PASSWORD@192.168.1.116:8080/h264_pcm.sdp\
&Monitor[V4LCapturesPerFrame]=1\
&Monitor[RTSPDescribe]=false\
&Monitor[Width]=1280\
&Monitor[Height]=720\
&Monitor[Colours]=4\
&Monitor[SaveJPEGs]=1\
&Monitor[VideoWriter]=0\
&Monitor[ImageBufferCount]=30\
&Monitor[WarmupCount]=0\
&Monitor[PreEventCount]=5\
&Monitor[PostEventCount]=5\
&Monitor[StreamReplayBuffer]=0\
&Monitor[LabelFormat]=\
&Monitor[AlarmFrameCount]=1"

# setup the zones for alarm detection of events
# https://zoneminder.readthedocs.io/en/latest/api.html#create-a-zone
# https://zoneminder.readthedocs.io/en/latest/userguide/definezone.html
# load up working zones, then load up https://192.168.1.226:9443/zm/api/zones.json to see the correct values
# note the coordinates are off by 1 since it starts at 0,0

# 2688 * 1520 = 4085760 (Area)
# 163430 / 4085760 = 0.0399 (MinAlarmPixels)
# 81715 / 4085760 = 0.0199 (MinFilterPixels)
curl --insecure -X POST https://192.168.1.226:9443/zm/api/zones.json -d "Zone[Name]=All\
&Zone[MonitorId]=1\
&Zone[Type]=Active\
&Zone[Units]=Pixels\
&Zone[NumCoords]=4\
&Zone[Coords]=0,0 2687,0 2687,1519 0,1519\
&Zone[Area]=4085760\
&Zone[AlarmRGB]=16711680\
&Zone[CheckMethod]=AlarmedPixels\
&Zone[MinPixelThreshold]=20\
&Zone[MaxPixelThreshold]=\
&Zone[MinAlarmPixels]=163430\
&Zone[MaxAlarmPixels]=\
&Zone[FilterX]=3\
&Zone[FilterY]=3\
&Zone[MinFilterPixels]=81715\
&Zone[MaxFilterPixels]=\
&Zone[MinBlobPixels]=\
&Zone[MaxBlobPixels]=\
&Zone[MinBlobs]=1\
&Zone[MaxBlobs]=\
&Zone[OverloadFrames]=0"

# 1280 * 720 = 921600 (Area)
# 36864 / 921600 = 0.04 (MinAlarmPixels)
# 18432 / 921600 = 0.02 (MinFilterPixels)
curl --insecure -X POST https://192.168.1.226:9443/zm/api/zones.json -d "Zone[Name]=All\
&Zone[MonitorId]=2\
&Zone[Type]=Active\
&Zone[Units]=Pixels\
&Zone[NumCoords]=4\
&Zone[Coords]=0,0 1279,0 1279,719 0,719\
&Zone[Area]=921600\
&Zone[AlarmRGB]=16711680\
&Zone[CheckMethod]=AlarmedPixels\
&Zone[MinPixelThreshold]=20\
&Zone[MaxPixelThreshold]=\
&Zone[MinAlarmPixels]=36864\
&Zone[MaxAlarmPixels]=\
&Zone[FilterX]=3\
&Zone[FilterY]=3\
&Zone[MinFilterPixels]=18432\
&Zone[MaxFilterPixels]=\
&Zone[MinBlobPixels]=\
&Zone[MaxBlobPixels]=\
&Zone[MinBlobs]=1\
&Zone[MaxBlobs]=\
&Zone[OverloadFrames]=0"