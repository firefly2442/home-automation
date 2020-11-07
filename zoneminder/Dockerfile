FROM localhost:5000/zoneminder:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
    nano curl ca-certificates \
    && apt-get -y upgrade \
    && rm -rf /var/lib/apt/lists/*

COPY cert.crt /usr/local/share/ca-certificates/cert.crt
COPY cert.key /usr/local/share/ca-certificates/cert.key
COPY ServerName /usr/local/share/ca-certificates/ServerName

COPY startup.sh /startup.sh
RUN chmod +x /startup.sh

CMD ["/startup.sh"]