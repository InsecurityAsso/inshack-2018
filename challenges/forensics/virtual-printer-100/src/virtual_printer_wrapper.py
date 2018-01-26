#!/usr/bin/env python3
# -!- encoding:utf-8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: dna_decoder_wrapper.py
#    date: 2017-08-30
#  author: paul.dautry
# purpose:
#      Wrapper for virtual printer script
# license:
#      GPLv3
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
#===============================================================================
import os
import sys
import signal
import redis
import base64
from uuid           import uuid4
from http.server    import HTTPServer
from http.server    import BaseHTTPRequestHandler
from subprocess     import check_output
from threading      import Thread
#===============================================================================
# CONFIGURATION
#===============================================================================
HOST = 'localhost'
PORT = 24042
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
TMP_DIR = 'tmp/'
WELCOME = """
<html>
    <head>
        <title>Virtual Printer Service</title>
    </head>
    <body>
        <pre>
+------------------------------------------------------------------------------+
|                                                                              |
|                          Virtual Printer Service !                           |
|                                                                              | 
+------------------------------------------------------------------------------+
|                              ________________                                |
|                            _/_______________/|                               |
|                           /___________/___//||   <- yes it's a printer :/    |
|                          |===        |----| ||                               |
|                          |           |   o| ||                               |
|                          |___________|   o| ||                               |
|                          | ||/.'---.||    | ||                               |
|                          |-||/_____\||-.  | |'                               |
|                          |_||=L==H==||_|__|/                                 |
|                                                                              |
+------------------------------------------------------------------------------+
|                                                                              |
|                               INSTRUCTIONS                                   |
|                                                                              |
+------------------------------------------------------------------------------+
|                                                                              |
| HEAD                                                                         |
|   > gives you the server headers. (useless)                                  |
|                                                                              |
|   $> curl -I <url>                                                           |
|                                                                              |
| GET                                                                          |
|   > /whatever/you/want...: gives you this page.                              |
|                                                                              |
|   $> curl <url>                                                              |
|                                                                              |
| POST                                                                         |
|   > /print: expects data to be a base64 encoded (RGB or RGBA) PNG file.      |
|   < you'll get your A4 page printed in the response as a base64 encoded PNG. |
|                                                                              |
|   $> curl -X POST --form "f=@<file.png.b64>" <url>                           |
|                                                                              |
|   > /serial-number: expects data to be a base64 encoded S/N                  |
|   < you'll get a flag if you're right                                        |
|                                                                              |
|   $> curl -X POST --data "sn=<b64encoded-serial-number>" <url>               |
|                                                                              |
+------------------------------------------------------------------------------+
        </pre>
        <pre style="visibility: hidden;">
            If y0u w4nn4 l34k, b3 sm4rt & st34lthy.
        </pre>
        <pre style="visibility: hidden;">
            Tested with curl 7.47.0
        </pre>
    </body>
</html>
"""
#===============================================================================
# CLASSES
#===============================================================================
class VPSDHandler(BaseHTTPRequestHandler):
    #---------------------------------------------------------------------------
    # __read_data
    #---------------------------------------------------------------------------
    def __read_data(self):
        data = None
        if 'Content-Length' in self.headers.keys():
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)
        return data
    #---------------------------------------------------------------------------
    # __debug_info
    #---------------------------------------------------------------------------
    def __debug_info(self):
        print('[INF] client_address: {0}'.format(self.client_address))
        print('[INF] command: {0}'.format(self.command))
        print('[INF] path: {0}'.format(self.path))
        print('[INF] headers:')
        print(self.headers)
    #---------------------------------------------------------------------------
    # __set_headers
    #---------------------------------------------------------------------------
    def __set_headers(self, code=200):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    #---------------------------------------------------------------------------
    # __save_secret
    #---------------------------------------------------------------------------
    def __save_secret(self, ip, secret):
        ip = 'vps-' + ip
        print('[INF] adding (ip, secret): ({0}, {1})'.format(ip, secret))
        REDIS_CONN.set(ip, secret) # register secret
        REDIS_CONN.expire(ip, 30) # valid for 30 seconds
    #---------------------------------------------------------------------------
    # __print
    #---------------------------------------------------------------------------
    def __print(self):
        ip = self.client_address[0]
        data = self.__read_data()
        b64 = data.split(b'\r\n')[4]
        try:
            img = base64.b64decode(b64)
        except:
            return '''
Error: could not find or decode base64 content.
Please upload data using the following command: curl -X POST --form "fileupload=@<file.png.b64>" http://...:.../print
'''
        tpath = os.path.join(TMP_DIR, '{0}.png'.format(uuid4()))
        with open(tpath, 'wb') as f:
            f.write(img)
        try:
            cmd = ['./virtual_printer.py', tpath, ip]
            print('[INF] running command: {0}'.format(cmd))
            output = check_output(cmd)
            os.remove(tpath)
        except:
            os.remove(tpath)
            return '''
Error: service failed to process your image. Try with another one.
If the problem persists with other images, please contact an admin.
            '''
        opath = output.split(b'\n')[0]
        secret = output.split(b'\n')[1]
        self.__save_secret(ip, secret)
        with open(opath, 'rb') as f:
            odata = f.read()
        os.remove(opath)
        return base64.b64encode(odata).decode('utf-8')
    #---------------------------------------------------------------------------
    # __serial_number
    #---------------------------------------------------------------------------
    def __serial_number(self):
        ip = self.client_address[0]
        data = self.__read_data()
        if data[0:3] == b'sn=':
            secret = data[3:]
            saved_secret = REDIS_CONN.get('vps-'+ip)
            if saved_secret is None:
                return 'Too late, you must submit your serial-number within a timeframe of 25 seconds after your image was printed.'
            elif secret == saved_secret:
                print('[INF] {0} gets a flag!'.format(ip))
                return 'Good job ! DO NOT LEAK SECRET FILES BY PRINTING THEM ! You can validate with: {0}'.format(FLAG)
            return 'Wrong secret... Try again :)'
        return '''
Error: could not find the serial number.
Please upload data using the following command: curl -X POST --data "sn=<b64encoded_serial_number>" http://...:.../serial-number
'''
    #---------------------------------------------------------------------------
    # handle HEAD requests
    #---------------------------------------------------------------------------
    def do_HEAD(self):
        self.__debug_info()
        self.__set_headers()
    #---------------------------------------------------------------------------
    # handle GET requests
    #---------------------------------------------------------------------------
    def do_GET(self):
        self.__debug_info()
        self.__set_headers()
        self.wfile.write(WELCOME.encode('utf-8'))
    #---------------------------------------------------------------------------
    # handle POST requests
    #---------------------------------------------------------------------------
    def do_POST(self):
        self.__debug_info()
        
        if self.path == '/print':
            resp = self.__print()
        elif self.path == '/serial-number':
            resp = self.__serial_number()
        else:
            resp = 'unknown path'
        self.__set_headers()
        self.wfile.write(resp.encode('utf-8'))
#-------------------------------------------------------------------------------
# VPSDServerThread
#-------------------------------------------------------------------------------
class VPSDServerThread(Thread):
    def __init__(self):
        super(VPSDServerThread, self).__init__()
        self.server = HTTPServer((HOST, PORT), VPSDHandler)

    def run(self):
        print('[INF] Server running on {0}:{1}'.format(HOST, PORT))
        self.server.serve_forever()

    def term(self):
        self.server.shutdown()
#===============================================================================
# GLOBALS
#===============================================================================
FLAG = None
SVR_THD = VPSDServerThread()
REDIS_CONN = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
#===============================================================================
# FUNCTIONS
#===============================================================================
def sigint_hdlr(signum, arg):
    SVR_THD.term()

def main():
    # load flag from external file
    global FLAG
    with open('flag.txt', 'r') as f:
        FLAG = f.read() 
        print('[INF] loaded flag: {0}'.format(FLAG))
        stop = 0
        while FLAG[stop] != '}':
            stop += 1
        FLAG = FLAG[:stop+1]
        print('[INF] processed flag: {0}'.format(FLAG))
    # make tmp/ directory
    os.makedirs(TMP_DIR, exist_ok=True)
    # test redis connection
    try:
        REDIS_CONN.set('foo', 'bar')
        REDIS_CONN.delete('foo')
        print('[INF] redis connection established and checked.')
    except Exception as e:
        print('[ERR] failed to interact with redis server. (host={0},port={1})'.format(
            REDIS_HOST, REDIS_PORT))
        exit(1)
    SVR_THD.start()
    SVR_THD.join()
#===============================================================================
# SCRIPT
#===============================================================================
if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_hdlr)
    main()
    exit(0)
