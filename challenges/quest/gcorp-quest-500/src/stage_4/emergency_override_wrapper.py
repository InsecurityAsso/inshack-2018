#!/usr/bin/env python3
# -!- encoding:utf-8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: emergency_override.py
#    date: 2017-08-30
#  author: paul.dautry
# purpose:
#      Stage 4 - Emergency Override
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
EO_SZ = 4
HOST = 'localhost'
PORT = 12042
FLAG = 'flag{...test...}'
#-------------------------------------------------------------------------------
# CLASSES
#-------------------------------------------------------------------------------
class EOHandler(BaseRequestHandler):
    def __send(self, msg):
        self.request.send(msg.encode('utf-8'))

    def handle(self):
        msg = """

                        G-Corp Emergency Override
                                 __    _
                            _wr""        "-q__
                         _dP                 9m_
                       _#P                     9#_
                      d#@                       9#m
                     d##                         ###
                    J###                         ###L
                    {###K                       J###A
                    ]####K      ___aaa___      J####F
                __gmM######_  w#P""   ""9#m  _d#####Mmw__
             _g##############mZ_         __g##############m_
           _d####M@PPPP@@M#######Mmp gm#########@@PPP9@M####m_
          a###""          ,Z"#####@" '######"\g          ""M##m
         J#@"             0L  "*##     ##@"  J#              *#K
         #"               `#    "_gmwgm_~    dF               `#_
        7F                 "#_   ]#####F   _dK                 JE
        ]                    *m__ ##### __g@"                   F
                               "PJ#####LP"
         `                       0######_                      '
                               _0########_
             .               _d#####^#####m__              ,
              "*w_________am#####P"   ~9#####mw_________w*"
                  ""9@#####@M""           ""P@#####@M""

Provide a valid override key:
"""
        self.__send(msg)
        key = self.request.recv(EO_SZ**3)
        try:
          output = check_output(['./emergency_override', 'check'], input=key)
        except Exception as e:
          output = b'KO'
        if b'OK' in output:
              msg = """

  Well done! You've just prevented doomsday... Awesome!

         888888ba                    dP     dP  dP   dP           .88888.
 dP dP   88    `8b                   88     88  88   88          d8'   `8b
8888888 a88aaaa8P' 88d888b. .d8888b. 88aaaaa88a 88aaa88 dP.  .dP 88     88 88d888b.
 88 88   88        88'  `88 88'  `88 88     88       88  `8bd8'  88     88 88'  `88
8888888  88        88       88.  .88 88     88       88  .d88b.  Y8.   .8P 88
 dP dP   dP        dP       `88888P' dP     dP       dP dP'  `dP  `8888P'  dP


  Good job! You must have this flag : %s

""" % FLAG
        else:
            msg = """

                           .ed''' '''$$$$be.
                         -'           ^''**$$$e.
                       .'                   '$$$c
                      /                      '4$$b
                     d  3                      $$$$
                     $  *                   .$$$$$$
                    .$  ^c           $$$$$e$$$$$$$$.
                    d$L  4.         4$$$$$$$$$$$$$$b
                    $$$$b ^ceeeee.  4$$ECL.F*$$$$$$$
        e$''=.      $$$$P d$$$$F $ $$$$$$$$$- $$$$$$
       z$$b. ^c     3$$$F '$$$$b   $'$$$$$$$  $$$$*'      .=''$c
      4$$$$L        $$P'  '$$b   .$ $$$$$...e$$        .=  e$$$.
      ^*$$$$$c  %..   *c    ..    $$ 3$$$$$$$$$$eF     zP  d$$$$$
        '**$$$ec   '   ece''    $$$  $$$$$$$$$$*    .r' =$$$$P''
              '*$b.  'c  *$e.    *** d$$$$$'L$$    .d'  e$$***'
                ^*$$c ^$c $$$      4J$$$$$% $$$ .e*'.eeP'
                   '$$$$$$''$=e....$*$$**$cz$$' '..d$*'
                     '*$$$  *=%4.$ L L$ P3$$$F $$$P'
                        '$   'e*ebJLzb$e$$$$$b $P'
                          %..      4$$$$$$$$$$ '
                           $$$e   z$$$$$$$$$$%
                            '*$c  '$$$$$$$P'
                             .'''*$$$$$$$$bc
                          .-''    .$***$$$'''*e.
                       .-'     .e'     '*$c  ^*b.
                .=*''''    .e$*'          '*bc  '*$e..
              .$'        .z*'               ^*$e.   '*****e.
              $$ee$c   .d'                     '*$.        3.
              ^*$E')$..$'                         *   .ee==d%
                 $.d$$$*                           *  J$$$e*
                  '''''                             ''$$$'

                                 R.I.P.

              You failed to save the world !!! Try again !
"""
        self.__send(msg)

class EOServerThread(Thread):
    def __init__(self):
        super(EOServerThread, self).__init__()
        self.server = ThreadingTCPServer((HOST, PORT), EOHandler)

    def run(self):
        self.server.serve_forever()

    def term(self):
        self.server.shutdown()
#-------------------------------------------------------------------------------
# GLOBALS
#-------------------------------------------------------------------------------
SVR_THD = EOServerThread()
#-------------------------------------------------------------------------------
# FUNCTIONS
#-------------------------------------------------------------------------------
def sigint_hdlr(signum, arg):
    SVR_THD.term()

def run():
    SVR_THD.start()
    SVR_THD.join()

def compute():
    key = os.urandom(512)
    print("using key: %s" % key)
    out = check_output(['./emergency_override', 'compute'], input=key).decode('utf-8')
    with open('key.bin', 'wb') as f:
        f.write(key)
    with open('key.result', 'w') as f:
        f.write(out)
    print(out)

def main():
    if len(sys.argv) != 2:
        print('usage: %s (run|compute)' % sys.argv[0])
        exit(1)
    if sys.argv[1] == 'run':
        run()
    if sys.argv[1] == 'compute':
        compute()

#-------------------------------------------------------------------------------
# SCRIPT
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    with open('flag.txt', 'r') as f:
        FLAG = f.read().split('\n')[0]
    signal.signal(signal.SIGINT, sigint_hdlr)
    main()
    exit(0)
