FROM ?

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install git python3 python3-dev pip3 && \
    git clone https://github.com/HugoDelval/inshack-2018 && \
    cd inshack-2018/quest/gcorp-stage-4/server-files/ && \
    pip3 install -r requirements.txt && \
    ./emergency_override_wrapper.py --config ../.mkctf.yml run

