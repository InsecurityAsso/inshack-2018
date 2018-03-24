#!/usr/bin/env sh

random=$(strings /dev/urandom | grep -o "[[:alnum:]]" | head -n 20 | /usr/bin/tr -d "\n")
image="gcorp-2-pwned-${1}-${random}"

timeout --kill-after=6 5 docker run --rm \
       -i \
       --name ${image} \
       --cpus=".1" \
       --memory=64m \
       --memory-swap=64m \
       --ulimit nproc=1024:1024 \
       --ulimit fsize=10000:10000 \
       --ulimit nofile=1024:2048 \
       --ulimit nice=1 \
       registry.dev.insecurity-insa.fr/insecurity/gcorp-stage-2-pwned
