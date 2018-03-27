FROM ubuntu

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3 python3-pip redis-server

ADD server-files/requirements.txt /tmp

RUN pip3 install --no-cache -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt && \
    mkdir -p /srv/app

ADD server-files/virtual_printer* .mkctf.yml /srv/app/
RUN useradd vp && \
    chown vp:vp /srv/app -R

WORKDIR /srv/app/

EXPOSE 24042

CMD service redis-server start && \
    su -c "./virtual_printer_wrapper.py --config .mkctf.yml" vp
