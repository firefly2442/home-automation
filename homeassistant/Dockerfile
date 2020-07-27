FROM homeassistant/home-assistant:stable

RUN apk add --no-cache \
    python3 py3-pip ca-certificates

RUN pip3 install --no-cache-dir requests

COPY *.py /

COPY cert.crt /usr/local/share/ca-certificates/cert.crt
COPY cert.key /usr/local/share/ca-certificates/cert.key

COPY startup.sh /startup.sh
RUN chmod +x /startup.sh

CMD ["/startup.sh"]