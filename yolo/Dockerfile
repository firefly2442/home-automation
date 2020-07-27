FROM tensorflow/tensorflow:latest-gpu

RUN apt-get update && apt-get install -y --no-install-recommends \
    nano libsm6 libxext6 libxrender-dev ca-certificates && \
    DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata \
    && apt-get -y upgrade \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir keras opencv-python pillow paho-mqtt configparser pyinstrument

WORKDIR /

COPY cert.crt /usr/local/share/ca-certificates/cert.crt
COPY cert.key /usr/local/share/ca-certificates/cert.key

COPY startup.sh startup.sh
RUN chmod +x startup.sh

RUN update-ca-certificates

COPY *.weights /yolo/

COPY ./yolov3-tf2/ /yolo/yolov3-tf2/

RUN python3 /yolo/yolov3-tf2/convert.py --weights /yolo/yolov3.weights --output /yolo/yolov3-tf2/checkpoints/yolov3.tf
RUN python3 /yolo/yolov3-tf2/convert.py --weights /yolo/yolov3-tiny.weights --output /yolo/yolov3-tf2/checkpoints/yolov3-tiny.tf --tiny

RUN rm /yolo/yolov3.weights /yolo/yolov3-tiny.weights

COPY *.py /


CMD ["./startup.sh"]
