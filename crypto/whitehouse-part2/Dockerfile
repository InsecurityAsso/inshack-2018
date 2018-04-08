FROM ubuntu

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y ucspi-tcp

ADD public-files/white-house-insecurity /
RUN useradd whitehouse

USER whitehouse
EXPOSE 18470

CMD tcpserver -v -c 300 -t 3 0.0.0.0 18470 /white-house-insecurity "INSA{Soci4l_engin33ring_w0uld_h4ve_w0rked_t00_I_gu3ss}" 49ad54d46d2fee35287d419edecb7260
