FROM ubuntu:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
    nano python3 python3-pip gifsicle curl && \
    DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata \
    && apt-get -y upgrade \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir flask requests imageio pygifsicle

COPY startup.sh startup.sh
RUN chmod +x startup.sh

COPY *.py /
COPY ./templates/*.html /templates/

CMD ["./startup.sh"]