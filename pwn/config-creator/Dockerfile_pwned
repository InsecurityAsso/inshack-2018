FROM python

RUN mkdir -p /srv/app && \
    useradd config-creator

ADD server-files/flag.txt server-files/app.py /srv/app/
RUN chown -R config-creator:config-creator /srv/app

WORKDIR /srv/app
USER config-creator

CMD python3 app.py
