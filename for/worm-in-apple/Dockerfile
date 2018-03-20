FROM ubuntu

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3 python3-dev python3-pip

ADD server-files/requirements.txt /tmp

RUN pip3 install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt && \
    mkdir -p /srv/app

ADD server-files/favicon.ico server-files/server.py .mkctf.yml /srv/app/
RUN useradd wia && \
    chown wia:wia /srv/app -R

WORKDIR /srv/app/
USER wia

CMD ./server.py --config .mkctf.yml
