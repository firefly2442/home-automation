#!/bin/bash

# setups up all the options we need for Zoneminder

# load up working options, then load up https://192.168.1.113:8443/zm/api/configs.json to see the correct values
# https://zoneminder.readthedocs.io/en/latest/api.html#configuration-apis
curl --insecure -X POST https://192.168.1.113:8443/zm/api/configs/edit/ZM_TIMEZONE.json -d "Config[Value]=America/Denver"

curl --insecure -X POST https://192.168.1.113:8443/zm/api/configs/edit/ZM_OPT_USE_EVENTNOTIFICATION.json -d "Config[Value]=1"