FROM ubuntu

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y python3-pip aria2

ADD server-files/requirements-server.txt /tmp/
RUN pip3 install -r /tmp/requirements-server.txt

RUN mkdir -p /srv/app && \
    useradd curler

ADD server-files/flag.txt server-files/server.py /srv/app/
RUN chown -R curler:curler /srv/app

WORKDIR /srv/app
USER curler

EXPOSE 8888

CMD python3 server.py
