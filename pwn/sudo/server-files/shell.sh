#!/bin/bash -i
echo "Spawning your shell..."
timeout --kill-after=122 120 docker run \
        --rm -it \
        --cpus=.2 \
        --ulimit nproc=1024:1024 \
        --ulimit fsize=10000:10000 \
        --ulimit nofile=1024:2048 \
        --ulimit nice=1 \
        registry.dev.insecurity-insa.fr/insecurity/sudo-pwned
