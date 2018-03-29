FROM python:latest

RUN mkdir -p /var/www
COPY www/ /var/www/
RUN pip install flask && \
    useradd python-runner
WORKDIR /var/www/
USER python-runner
CMD ["python","/var/www/server.py"]
