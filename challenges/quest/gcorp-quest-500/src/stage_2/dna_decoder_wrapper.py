#!/usr/bin/env python3
# -!- encoding:utf-8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: dna_decoder_wrapper.py
#    date: 2017-08-30
#  author: paul.dautry
# purpose:
#      Stage 2 - G-Corp DNA Decoder
#         Wrapper for dna_decoder binary
# license:
#      GPLv3
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
#-------------------------------------------------------------------------------
import os
import sys
import signal
from socketserver import ThreadingTCPServer
from socketserver import BaseRequestHandler
from subprocess   import check_output
from threading    import Thread
#-------------------------------------------------------------------------------
# CONFIGURATION
#-------------------------------------------------------------------------------
HOST = 'localhost'
PORT = 12142
FLAG = 'unloaded_flag'
#-------------------------------------------------------------------------------
# CLASSES
#-------------------------------------------------------------------------------
class DNADHandler(BaseRequestHandler):
    def handle(self):
        msg = b"""

                        G-Corp DNA Decoder

    -._    _.--'"`'--._    _.--'"`'--._    _.--'"`'--._    _
        '-:`.'|`|"':-.  '-:`.'|`|"':-.  '-:`.'|`|"':-.  '.` : '.
      '.  '.  | |  | |'.  '.  | |  | |'.  '.  | |  | |'.  '.:   '.  '.
      : '.  '.| |  | |  '.  '.| |  | |  '.  '.| |  | |  '.  '.  : '.  `.
      '   '.  `.:_ | :_.' '.  `.:_ | :_.' '.  `.:_ | :_.' '.  `.'   `.
             `-..,..-'       `-..,..-'       `-..,..-'       `         `


Provide valid DNA data please (limited to 1024 bytes):
"""
        self.request.send(msg)
        data = self.request.recv(1024)
        try:
          output = check_output(['./dna_decoder'], input=data)
        except Exception as e:
          pass
        self.request.send(output)

class DNADServerThread(Thread):
    def __init__(self):
        super(DNADServerThread, self).__init__()
        self.server = ThreadingTCPServer((HOST, PORT), DNADHandler)

    def run(self):
        self.server.serve_forever()

    def term(self):
        self.server.shutdown()
#-------------------------------------------------------------------------------
# GLOBALS
#-------------------------------------------------------------------------------
SVR_THD = DNADServerThread()
#-------------------------------------------------------------------------------
# FUNCTIONS
#-------------------------------------------------------------------------------
def sigint_hdlr(signum, arg):
    SVR_THD.term()

def main():
    SVR_THD.start()
    SVR_THD.join()
#-------------------------------------------------------------------------------
# SCRIPT
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_hdlr)
    main()
    exit(0)
