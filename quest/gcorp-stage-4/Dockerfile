FROM ubuntu

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3 python3-pip

ADD server-files/requirements.txt /tmp

RUN pip3 install --no-cache -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt && \
    mkdir -p /srv/app

ADD server-files/emergency_override* .mkctf.yml /srv/app/
RUN useradd gcorp && \
    chown gcorp:gcorp /srv/app -R

WORKDIR /srv/app/
USER gcorp

EXPOSE 12042

CMD ./emergency_override_wrapper.py --config .mkctf.yml run
