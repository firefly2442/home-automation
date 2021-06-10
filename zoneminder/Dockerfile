FROM ubuntu:20.04

# examples and docs
# https://github.com/ZoneMinder/zmdockerfiles/blob/master/release/ubuntu18.04/Dockerfile
# https://zoneminder.readthedocs.io/en/stable/installationguide/ubuntu.html#easy-way-ubuntu-18-04-bionic

# https://launchpad.net/~iconnor/+archive/ubuntu/zoneminder-master?field.series_filter=focal
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    nano curl ca-certificates lsof gnupg software-properties-common file && \
    apt-get -y upgrade
RUN add-apt-repository ppa:iconnor/zoneminder-master && \
    apt-get install -y --no-install-recommends \
    zoneminder apache2 php libapache2-mod-php php-mysql && \
    rm -rf /var/lib/apt/lists/*

COPY cert.crt /usr/local/share/ca-certificates/cert.crt
COPY cert.key /usr/local/share/ca-certificates/cert.key
COPY ServerName /usr/local/share/ca-certificates/ServerName

COPY ssl.conf /etc/apache2/sites-available/ssl.conf

# ssl is /etc/apache2/sites-available/ssl.conf
RUN a2enconf zoneminder && \
    a2enmod rewrite cgi && \
    a2enmod ssl && \
    a2enmod headers && \
    a2ensite ssl && \
    apache2ctl configtest

COPY *.sh /
RUN chmod +x /*.sh

CMD ["/startup.sh"]