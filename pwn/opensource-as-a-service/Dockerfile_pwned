FROM ubuntu

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y python3-pip libssl-dev ssh

RUN locale-gen en_US.UTF-8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'

ADD server-files/requirements.txt /tmp

RUN pip3 install --no-cache -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt && \
    mkdir -p /srv/app && \
    useradd osaas

ADD server-files/flag.txt server-files/app.py /srv/app/
RUN chown -R osaas:osaas /srv/app

WORKDIR /srv/app
USER osaas

CMD python3 app.py
