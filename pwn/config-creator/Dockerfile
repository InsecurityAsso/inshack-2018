FROM ubuntu

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y docker.io ucspi-tcp pwgen cron

ADD server-files/shell.sh /

RUN echo '* * * * * root docker kill $(docker ps -f "name=config-creator-pwned" -f "status=running" | grep -P "Up \d+ minutes" | cut -d" " -f 1)' >> /etc/crontab && \
    echo >> /etc/crontab


EXPOSE 10000

CMD docker login -u ${DOCKER_USER} -p ${DOCKER_PASSWORD} registry-chal.infra.insecurity-insa.fr && \
    service cron start && \
    tcpserver -v -c 300 -t 3 0.0.0.0 10000 /shell.sh
