#/bin/bash

# TODO: replace with this already converted file?
# https://github.com/OlafenwaMoses/ImageAI/releases/tag/1.0
if [ ! -f "/yolo/model.h5" ]; then
    python3 prepmodel.py
fi

python3 yolo.py