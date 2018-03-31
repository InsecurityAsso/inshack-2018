FROM python:latest

RUN mkdir -p /var/www
COPY www/ /var/www/
RUN pip install flask && \
    apt-get update && \
    apt-get install -y tesseract-ocr &&\
    pip install pytesseract &&\
    pip install flask_recaptcha &&\
    useradd python-runner
WORKDIR /var/www/
USER python-runner
CMD ["python","/var/www/server.py"]
