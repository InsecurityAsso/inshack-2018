#!/bin/bash -i
rndm=$(pwgen 20 1)
name="curler-pwned-${rndm}"
echo "Launching your app.."
timeout --kill-after=132 130 docker run \
        --rm \
        --name=${name} \
        --cpus=.1 \
        --memory=64m \
        --memory-swap=128m \
        --ulimit nproc=1024:1024 \
        --ulimit fsize=10000:10000 \
        --ulimit nofile=1024:2048 \
        --ulimit nice=1 \
        registry-chal.infra.insecurity-insa.fr/insecurity/curler-pwned &

echo "5.."
sleep 1
echo "4.."
sleep 1
echo "3.."
sleep 1
echo "2.."
sleep 1
echo "1.."
sleep 1
su -c "timeout --kill-after=122 120 python3 wrapper.py ${name}" curler
docker kill ${name} >/dev/null 2>&1 || exit 0
