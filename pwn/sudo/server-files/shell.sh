#!/bin/bash -i
echo "Spawning your shell..."
sh /tmp/login >/dev/null 2>&1
name=$(pwgen 20 1)
timeout --kill-after=122 120 docker run \
        --rm -it \
        --name=sudo-pwned-${name} \
        --cpus=.2 \
        --ulimit nproc=1024:1024 \
        --ulimit fsize=10000:10000 \
        --ulimit nofile=1024:2048 \
        --ulimit nice=1 \
        registry-chal.infra.insecurity-insa.fr/insecurity/sudo-pwned

docker kill ${name} >/dev/null 2>&1 || exit 0
