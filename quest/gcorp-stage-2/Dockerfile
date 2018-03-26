FROM ubuntu

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3 python3-dev python3-pip docker.io

ADD server-files/requirements.txt /tmp

RUN pip3 install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt && \
    mkdir -p /srv/app

ADD server-files/dna_decoder_wrapper.py server-files/docker_wrapper.sh .mkctf.yml /srv/app/

WORKDIR /srv/app/

EXPOSE 80

CMD docker login -u ${DOCKER_USER} -p ${DOCKER_PASSWORD} registry.dev.insecurity-insa.fr && \
    ./dna_decoder_wrapper.py --config .mkctf.yml
