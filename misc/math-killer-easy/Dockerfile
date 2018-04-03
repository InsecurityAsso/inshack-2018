FROM python:latest

RUN pip install flask gunicorn && \
    useradd python-runner

RUN mkdir -p /srv/app

COPY src/ /srv/app

WORKDIR /srv/app
RUN chown -R python-runner:python-runner /srv/app

USER python-runner

EXPOSE 5000

CMD gunicorn -b 0.0.0.0:5000 --access-logfile=- --error-logfile=- server:app
