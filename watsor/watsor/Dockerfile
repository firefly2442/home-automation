# dockerhub version
FROM smirnou/watsor.gpu:latest
# our custom version
#ROM watsor.gpu:latest

USER root

# use inception v2 over mobilenet v2, seems to be a little more accurate at the expense of computation
RUN mkdir model && \
    wget -q https://github.com/asmirnou/todus/raw/models/ssd_inception_v2_coco_2018_01_28.uff -O model/gpu.uff && \
    mv model/gpu.uff /usr/share/watsor/model && \
    chown watsor:watsor /usr/share/watsor/model/gpu.uff && \
    rm -r model


USER watsor