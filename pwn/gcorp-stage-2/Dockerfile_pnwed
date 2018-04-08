FROM alpine

RUN mkdir -p /srv/app

ADD server-files/.flag.txt server-files/dna_decoder server-files/stage_3_storage.zip /srv/app/
RUN adduser -S gcorp && \
    chown gcorp /srv/app -R

WORKDIR /srv/app/
USER gcorp

CMD ./dna_decoder
