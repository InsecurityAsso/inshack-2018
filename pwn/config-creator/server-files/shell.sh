#!/bin/bash -i
name="config-creator-pwned-$(pwgen 20 1)"
timeout --kill-after=122 120 docker run \
        --rm -i \
        --name=${name} \
        --cpus=.1 \
        --memory=64m \
        --memory-swap=128m \
        --ulimit nproc=1024:1024 \
        --ulimit fsize=10000:10000 \
        --ulimit nofile=1024:2048 \
        --ulimit nice=1 \
        registry-chal.infra.insecurity-insa.fr/insecurity/config-creator-pwned

docker kill ${name} >/dev/null 2>&1 || exit 0
