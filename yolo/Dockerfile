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

#TODO: debugging, swap back over when finished
#COPY *.h5 /yolo/

COPY ./yolov3-tf2/ /yolo/yolov3-tf2/

RUN python3 /yolo/yolov3-tf2/convert.py --weights /yolo/yolov3.weights --output /yolo/yolov3-tf2/checkpoints/yolov3.tf
RUN python3 /yolo/yolov3-tf2/convert.py --weights /yolo/yolov3-tiny.weights --output /yolo/yolov3-tf2/checkpoints/yolov3-tiny.tf --tiny


COPY *.py /

#RUN python3 convert.py /yolo/yolov3.cfg /yolo/yolov3.weights /yolo/model.h5
#RUN python3 convert.py /yolo/yolov3-tiny.cfg /yolo/yolov3-tiny.weights /yolo/model-tiny.h5


# for profiling
CMD ["python3", "-m", "pyinstrument", "yolo.py"]
# without profiling, no overhead
#CMD ["python3", "yolo.py"]