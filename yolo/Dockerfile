FROM tensorflow/tensorflow:latest-gpu-py3

RUN apt-get update && apt-get install -y \
    nano \
    libsm6 libxext6 libxrender-dev \
    && apt-get -y upgrade \
    && rm -rf /var/lib/apt/lists/*

RUN pip install keras opencv-python pillow paho-mqtt

WORKDIR /

COPY yolov3.weights /yolo/yolov3.weights

COPY *.py /

COPY run.sh /

CMD ["/bin/bash", "run.sh"]
