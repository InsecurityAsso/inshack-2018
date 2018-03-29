FROM ubuntu

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y docker.io ssh

ADD server-files/shell.sh /
RUN echo "/shell.sh" >> /etc/shells && \
    useradd -m -N -o -s /shell.sh -u 0 sudo && \
    touch /home/sudo/.hushlogin && \
    echo sudo:sudo | chpasswd

EXPOSE 22

CMD docker login -u ${DOCKER_USER} -p ${DOCKER_PASSWORD} registry.dev.insecurity-insa.fr && \
    mkdir -p /var/run/sshd && \
    /usr/sbin/sshd -e -D -o PermitRootLogin=yes
