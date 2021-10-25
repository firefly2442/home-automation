FROM homeassistant/home-assistant:stable

RUN apk add --no-cache \
    python3 py3-pip ca-certificates iputils

RUN pip3 install --no-cache-dir requests

#RUN mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys
RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh
COPY id_rsa /root/.ssh/id_rsa
COPY id_rsa.pub /root/.ssh/id_rsa.pub
RUN touch /root/.ssh/authorized_keys && chmod 600 /root/.ssh/authorized_keys && \
    touch /root/.ssh/known_hosts && chmod 600 /root/.ssh/known_hosts && \
    cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys && \
    ssh-keyscan -H 192.168.1.226 >> /root/.ssh/known_hosts

COPY cert.crt /usr/local/share/ca-certificates/cert.crt
COPY cert.key /usr/local/share/ca-certificates/cert.key

COPY startup.sh /startup.sh
RUN chmod +x /startup.sh

CMD ["/startup.sh"]