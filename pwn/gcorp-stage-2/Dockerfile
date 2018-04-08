FROM ubuntu

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3 python3-pip docker.io pwgen cron

ADD server-files/requirements.txt /tmp

RUN pip3 install --no-cache -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt && \
    mkdir -p /srv/app
RUN echo '* * * * * root docker kill $(docker ps -f "name=gcorp-stage-2-pwned" -f "status=running" | grep -P "Up \d+ minutes" | cut -d" " -f 1)' >> /etc/crontab && \
    echo >> /etc/crontab

ADD server-files/dna_decoder_wrapper.py server-files/docker_wrapper.sh .mkctf.yml /srv/app/

WORKDIR /srv/app/

EXPOSE 80

CMD docker login -u ${DOCKER_USER} -p ${DOCKER_PASSWORD} registry-chal.infra.insecurity-insa.fr && \
    docker pull registry-chal.infra.insecurity-insa.fr/insecurity/gcorp-stage-2-pwned && \
    service cron start && \
    ./dna_decoder_wrapper.py --config .mkctf.yml
