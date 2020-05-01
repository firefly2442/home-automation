FROM tensorflow/tensorflow:latest-gpu-py3

RUN apt-get update && apt-get install -y \
    nano \
    libsm6 libxext6 libxrender-dev \
    && apt-get -y upgrade \
    && rm -rf /var/lib/apt/lists/*

RUN pip install keras opencv-python pillow paho-mqtt configparser pyinstrument

WORKDIR /

COPY *.weights /yolo/

COPY *.cfg /yolo/

COPY *.py /

RUN [ -e "/yolo/model.h5" ] && echo "/yolo/model.h5 already generated" || python3 convert.py /yolo/yolov3.cfg /yolo/yolov3.weights /yolo/model.h5

RUN [ -e "/yolo/model-tiny.h5" ] && echo "/yolo/model-tiny.h5 already generated" || python3 convert.py /yolo/yolov3-tiny.cfg /yolo/yolov3-tiny.weights /yolo/model-tiny.h5

CMD ["python3", "yolo.py"]