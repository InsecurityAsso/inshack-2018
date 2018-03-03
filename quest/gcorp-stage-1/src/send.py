#!/usr/bin/env python3
# -!- encoding:utf8 -!-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: send.py
#     date: 2018-03-03
#   author: paul.dautry
#  purpose:
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  IMPORTS
# =============================================================================
import os
import base64
import socket
from ruamel import yaml
from argparse import ArgumentParser
# =============================================================================
#  FUNCTIONS
# =============================================================================
##
## @brief      { function_description }
##
## @param      host      The host
## @param      port      The port
## @param      content   The content
##
def netcat(host, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(content)
    s.close()
##
## @brief      Reads a file.
##
def read_file(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    return data
##
## @brief      Gets the flag.
##
def get_flag(config):
    with open(config, 'r') as f:
        conf = yaml.safe_load(f)
    return conf['flag']
##
## @brief      { function_description }
##
def main():
    p = ArgumentParser(add_help=True,
                       description="Prepares GCorp - Stage 1 challenge.")
    p.add_argument('host', help="Remote ip.")
    p.add_argument('port', type=int, help="Remote listening port.")
    p.add_argument('-c', '--config', default='.mkctf.yml')
    args = p.parse_args()

    print('[send.py]> preparing payload...', end='')
    payload = b''
    payload += os.urandom(3631)  # grabage 1
    payload += read_file('logo.png')
    payload += os.urandom(8056)  # grabage 2
    payload += read_file('r34dm3.txt')
    payload += os.urandom(5058)  # grabage 3
    payload += read_file('dna_decoder')
    payload += os.urandom(4242)  # grabage 4
    payload += base64.b64encode(get_flag(args.config).encode())
    print('done!')

    print('[send.py]> sending payload...', end='')
    netcat(args.host, args.port, payload)
    print('done!')
# =============================================================================
#  SCRIPT
# =============================================================================
if __name__ == '__main__':
    main()
