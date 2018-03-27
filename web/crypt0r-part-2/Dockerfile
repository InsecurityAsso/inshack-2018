FROM ubuntu

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y python3-pip

ADD server-files/requirements.txt /tmp
RUN pip3 install --no-cache -r /tmp/requirements.txt && rm /tmp/requirements.txt

RUN mkdir -p /srv/app && \
    useradd crypt0r

ADD server-files/ /srv/app/
RUN chown -R crypt0r:crypt0r /srv/app

WORKDIR /srv/app
USER crypt0r

EXPOSE 5000

CMD gunicorn app:app -b 0.0.0.0:5000 --access-logfile - --error-logfile -
