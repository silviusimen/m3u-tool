FROM ubuntu:20.04
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -y update && apt-get -y upgrade && apt-get install -q -y ca-cacert ca-certificates curl s-nail php ssh mc bash net-tools iputils-ping apache2 php-mysql php-xml php-tidy libapache2-mod-php php-ds
RUN apt-get -y clean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN a2enmod php7.4
CMD /usr/sbin/apache2ctl -D FOREGROUND & tail -f /var/log/apache2/error.log
#CMD /bin/bash