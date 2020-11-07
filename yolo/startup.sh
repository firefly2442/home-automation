#!/bin/bash

# https://stackoverflow.com/questions/61065541/importerror-usr-lib-aarch64-linux-gnu-libgomp-so-1-cannot-allocate-memory-in
# get around error
# ImportError: /lib/aarch64-linux-gnu/libgomp.so.1: cannot allocate memory in static TLS block
export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1:/$LD_PRELOAD

# for profiling
#python3 -m pyinstrument yolo.py
# without profiling, no overhead
python3 yolo.py