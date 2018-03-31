FROM ubuntu

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y docker.io ssh pwgen cron

ADD server-files/shell.sh /
RUN echo "/shell.sh" >> /etc/shells && \
    useradd -m -N -o -s /shell.sh -u 0 sudo && \
    touch /home/sudo/.hushlogin && \
    echo sudo:sudo | chpasswd && \
    echo '* * * * * root docker kill $(docker ps -f "name=sudo-pwned" -f "status=running" | grep -P "Up \d+ minutes" | cut -d" " -f 1)' >> /etc/crontab && \
    echo >> /etc/crontab

EXPOSE 22

CMD docker login -u ${DOCKER_USER} -p ${DOCKER_PASSWORD} registry.dev.insecurity-insa.fr && \
    service cron start && \
    mkdir -p /var/run/sshd && \
    /usr/sbin/sshd -e -D -o PermitRootLogin=yes
