FROM python:latest

RUN pip install flask gunicorn ruamel.yaml && \
    useradd python-runner

RUN mkdir -p /var/www

COPY server-files/ /var/www/
COPY .mkctf.yml /var/www/

WORKDIR /var/www/
RUN chown -R python-runner:python-runner /var/www/

USER python-runner

EXPOSE 5000

CMD gunicorn -b 0.0.0.0:5000 --access-logfile=- --error-logfile=- server:app
