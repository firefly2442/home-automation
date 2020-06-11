FROM tensorflow/tensorflow:latest-gpu-py3

RUN apt-get update && apt-get install -y --no-install-recommends \
    nano libsm6 libxext6 libxrender-dev && \
    DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata \
    && apt-get -y upgrade \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir keras opencv-python pillow paho-mqtt configparser pyinstrument

WORKDIR /

COPY *.weights /yolo/

COPY ./yolov3-tf2/ /yolo/yolov3-tf2/

RUN python3 /yolo/yolov3-tf2/convert.py --weights /yolo/yolov3.weights --output /yolo/yolov3-tf2/checkpoints/yolov3.tf
RUN python3 /yolo/yolov3-tf2/convert.py --weights /yolo/yolov3-tiny.weights --output /yolo/yolov3-tf2/checkpoints/yolov3-tiny.tf --tiny

RUN rm /yolo/yolov3.weights /yolo/yolov3-tiny.weights

COPY *.py /

# for profiling
#CMD ["python3", "-m", "pyinstrument", "yolo.py"]
# without profiling, no overhead
CMD ["python3", "yolo.py"]
