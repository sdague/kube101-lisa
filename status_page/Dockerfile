FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV FLASK_APP status_page
ENV STATUS_PAGE_SETTINGS ../settings.cfg

RUN apt-get update && apt-get install -y python3 python3-dev python3-pip && apt-get clean

COPY ./ /var/www/status_page
WORKDIR /var/www/status_page

RUN pip3 install -U .

CMD flask run -h 0.0.0.0
