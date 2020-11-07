# focal = 20.04
FROM ubuntu:focal

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-dev python3-numpy python3-opencv python3-scipy python3-h5py libhdf5-dev libatlas-base-dev git \
    nano libsm6 libxext6 libxrender-dev ca-certificates sudo \
    gfortran libc-ares-dev libeigen3-dev \
    libopenblas-dev libblas-dev liblapack-dev build-essential && \
    DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata \
    && apt-get -y upgrade \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir keras pillow paho-mqtt configparser

RUN pip3 install --upgrade setuptools

RUN pip3 install --no-cache-dir pybind11 Cython==0.29.21 h5py pyinstrument

# https://qengineering.eu/install-tensorflow-2.3.1-on-raspberry-64-os.html
# https://github.com/Qengineering/TensorFlow-Raspberry-Pi_64-bit
COPY tensorflow-2.3.1-cp38-cp38-linux_aarch64.whl /tensorflow-2.3.1-cp38-cp38-linux_aarch64.whl

RUN pip3 install --no-cache-dir tensorflow-2.3.1-cp38-cp38-linux_aarch64.whl && \
    rm tensorflow-2.3.1-cp38-cp38-linux_aarch64.whl

WORKDIR /

COPY cert.crt /usr/local/share/ca-certificates/cert.crt
COPY cert.key /usr/local/share/ca-certificates/cert.key

RUN update-ca-certificates

COPY *.weights /yolo/

COPY ./yolov3-tf2/ /yolo/yolov3-tf2/

# https://stackoverflow.com/questions/61065541/importerror-usr-lib-aarch64-linux-gnu-libgomp-so-1-cannot-allocate-memory-in
# get around error
# ImportError: /lib/aarch64-linux-gnu/libgomp.so.1: cannot allocate memory in static TLS block

RUN export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1:/$LD_PRELOAD && \
    python3 /yolo/yolov3-tf2/convert.py --weights /yolo/yolov3.weights --output /yolo/yolov3-tf2/checkpoints/yolov3.tf
RUN export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1:/$LD_PRELOAD && \
    python3 /yolo/yolov3-tf2/convert.py --weights /yolo/yolov3-tiny.weights --output /yolo/yolov3-tf2/checkpoints/yolov3-tiny.tf --tiny

RUN rm /yolo/yolov3.weights /yolo/yolov3-tiny.weights

COPY startup.sh startup.sh
RUN chmod +x startup.sh

COPY *.py /

CMD ["./startup.sh"]
