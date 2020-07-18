FROM homeassistant/home-assistant:stable

RUN apk add --no-cache \
    python3 py3-pip

RUN pip3 install --no-cache-dir requests

COPY *.py /

COPY startup.sh /startup.sh
RUN chmod +x /startup.sh

CMD ["/startup.sh"]