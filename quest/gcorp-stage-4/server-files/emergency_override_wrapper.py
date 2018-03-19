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
import asyncio
import os
from ruamel import yaml
from argparse import ArgumentParser
from subprocess import check_output
from tornado.web import Application, RequestHandler
from tornado.log import access_log, enable_pretty_logging
from tornado.options import options, parse_command_line
from tornado.platform.asyncio import AsyncIOMainLoop
#-------------------------------------------------------------------------------
# CONSTANTS
#-------------------------------------------------------------------------------
EO_SZ = 4
#-------------------------------------------------------------------------------
# CLASSES
#-------------------------------------------------------------------------------
class MainHandler(RequestHandler):
    ##
    ## @brief      { function_description }
    ##
    ## @param      flag  The flag
    ##
    def initialize(self, flag):
        self.flag = flag
    ##
    ## @brief      { function_description }
    ##
    def get(self):
        self.write(b"""

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

POST a valid override key.
""")
        self.finish()
    ##
    ## @brief      { function_description }
    ##
    def post(self):
        key = self.request.body[:EO_SZ**3]

        try:
            output = check_output(['./emergency_override', 'check'], input=key)
        except Exception as e:
            access_log.exception("An exception occured...")
            self.set_status(500)
            self.write("An exception occured, feel free to contact an admin.")
            self.finish()
            return

        if b'OK' in output:
            msg = """

  Well done! You've just prevented doomsday... Awesome!

         888888ba                    dP     dP  dP   dP           .88888.
 dP dP   88    `8b                   88     88  88   88          d8'   `8b
8888888 a88aaaa8P' 88d888b. .d8888b. 88aaaaa88a 88aaa88 dP.  .dP 88     88 88d888b.
 88 88   88        88'  `88 88'  `88 88     88       88  `8bd8'  88     88 88'  `88
8888888  88        88       88.  .88 88     88       88  .d88b.  Y8.   .8P 88
 dP dP   dP        dP       `88888P' dP     dP       dP dP'  `dP  `8888P'  dP


  Good job! You must have this flag : {}

""".format(self.flag)
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
        self.write(msg.encode())
        self.finish()
#------------------------------------------------------------------------------
# FUNCTIONS
#------------------------------------------------------------------------------
##
## @brief      { function_description }
##
def compute():
    key = os.urandom(512)

    print("using key: {}".format(key))
    out = check_output(['./emergency_override', 'compute'], input=key)

    with open('key.bin', 'wb') as f:
        f.write(key)

    with open('key.result', 'wb') as f:
        f.write(out)

    print(out)
##
## @brief      { function_description }
##
def run():
    options.logging = 'info'
    parse_command_line(args=[])
    enable_pretty_logging()

    with open(args.config, 'r') as f:
        conf = yaml.safe_load(f)

    parameters = conf['parameters']

    AsyncIOMainLoop().install()

    app = Application([
        (r"/", MainHandler, dict(flag=conf['flag']))
    ], debug=args.debug)

    app.listen(parameters['port'])

    asyncio.get_event_loop().run_forever()
#-------------------------------------------------------------------------------
# SCRIPT
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    p = ArgumentParser(add_help=True,
                       description="Emergency Override Server.")
    p.add_argument('command', choices=['run', 'compute'],
                   help="starts the server or compute a new result using a "
                        "random key.")
    p.add_argument('-d', '--debug', action='store_true',
                   help="turns on debug mode.")
    p.add_argument('-c', '--config', default='.mkctf.yml',
                   help="mkctf configuration file.")
    args = p.parse_args()

    if args.command == 'run':
        run()
    elif args.command == 'compute':
        compute()


