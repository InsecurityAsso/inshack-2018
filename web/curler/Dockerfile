FROM ubuntu

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y docker.io ucspi-tcp pwgen cron python3-pip

ADD server-files/requirements-wrapper.txt /tmp/
RUN pip3 install -r /tmp/requirements-wrapper.txt

ADD server-files/shell.sh /

RUN mkdir -p /srv/app && \
    useradd curler && \
    echo '* * * * * root docker kill $(docker ps -f "name=curler-pwned" -f "status=running" | grep -P "Up \d+ minutes" | cut -d" " -f 1)' >> /etc/crontab && \
    echo >> /etc/crontab

ADD server-files/wrapper.py /srv/app/
RUN chown -R curler /srv/app/

WORKDIR /srv/app

EXPOSE 10001

CMD docker login -u ${DOCKER_USER} -p ${DOCKER_PASSWORD} registry-chal.infra.insecurity-insa.fr && \
    service cron start && \
    tcpserver -v -c 300 -t 3 0.0.0.0 10001 /shell.sh
