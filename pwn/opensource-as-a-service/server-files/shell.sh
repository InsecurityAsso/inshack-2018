#!/bin/bash -i
name="opensource-as-a-service-pwned-$(pwgen 20 1)"
echo "Spawning your shell..."
timeout --kill-after=122 120 docker run \
        --rm -i \
        --name=${name} \
        --cpus=.2 \
        --memory=128m \
        --memory-swap=128m \
        --ulimit nproc=1024:1024 \
        --ulimit fsize=10000:10000 \
        --ulimit nofile=1024:2048 \
        --ulimit nice=1 \
        registry-chal.infra.insecurity-insa.fr/insecurity/opensource-as-a-service-pwned

docker kill ${name} >/dev/null 2>&1 || exit 0
