FROM ubuntu

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y libssl-dev

WORKDIR /srv/app/

RUN mkdir -p /srv/app && \
    useradd sudo-pwned && \
    useradd -N -g sudo-pwned sudo

ADD server-files/flag.txt server-files/sudo /srv/app/
RUN chown -R sudo-pwned:sudo-pwned /srv/app && \
    chmod 400 /srv/app/flag.txt && \
    chmod 4550 /srv/app/sudo

WORKDIR /srv/app
USER sudo

CMD bash
