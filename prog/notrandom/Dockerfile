FROM python:latest

RUN pip install ruamel.yaml

RUN mkdir -p /var/www && \
    useradd python-runner

COPY server-files/ /var/www/
COPY .mkctf.yml /var/www/

WORKDIR /var/www/
EXPOSE 10002
USER python-runner

CMD ["python","/var/www/server.py"]
