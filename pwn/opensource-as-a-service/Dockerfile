FROM ubuntu


RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y docker.io ucspi-tcp

EXPOSE 12345

CMD docker login -u ${DOCKER_USER} -p ${DOCKER_PASSWORD} registry.dev.insecurity-insa.fr && \
    tcpserver -v -c 300 -t 3 0.0.0.0 12345 \
        timeout --kill-after=122 120 docker run \
            --rm -i \
            --cpus=.2 \
            --memory=128m \
            --memory-swap=128m \
            --ulimit nproc=1024:1024 \
            --ulimit fsize=10000:10000 \
            --ulimit nofile=1024:2048 \
            --ulimit nice=1 \
            registry.dev.insecurity-insa.fr/insecurity/opensource-as-a-service-pwned
