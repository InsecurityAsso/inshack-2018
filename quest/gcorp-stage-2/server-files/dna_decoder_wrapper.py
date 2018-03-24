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
import asyncio
from ruamel import yaml
from argparse import ArgumentParser
from subprocess import run
from subprocess import PIPE
from tornado.web import Application, RequestHandler
from tornado.log import access_log, enable_pretty_logging
from tornado.options import options, parse_command_line
from tornado.platform.asyncio import AsyncIOMainLoop
#-------------------------------------------------------------------------------
# CLASSES
#-------------------------------------------------------------------------------
##
## @brief      Class for main handler.
##
class MainHandler(RequestHandler):
    ##
    ## @brief      { function_description }
    ##
    def get(self):
        self.write(b"""

                        G-Corp DNA Decoder

    -._    _.--'"`'--._    _.--'"`'--._    _.--'"`'--._    _
        '-:`.'|`|"':-.  '-:`.'|`|"':-.  '-:`.'|`|"':-.  '.` : '.
      '.  '.  | |  | |'.  '.  | |  | |'.  '.  | |  | |'.  '.:   '.  '.
      : '.  '.| |  | |  '.  '.| |  | |  '.  '.| |  | |  '.  '.  : '.  `.
      '   '.  `.:_ | :_.' '.  `.:_ | :_.' '.  `.:_ | :_.' '.  `.'   `.
             `-..,..-'       `-..,..-'       `-..,..-'       `         `


POST valid DNA data (input limited to 1024 bytes).
""")
        self.finish()
    ##
    ## @brief      { function_description }
    ##
    def post(self):
        data = self.request.body
        # VULN: do not truncate input size
        try:
            client_ip = self.request.headers.get("X-Real-IP") or self.request.remote_ip
            output = run(['./docker_wrapper.sh', client_ip], input=data, stdout=PIPE).stdout
        except Exception as e:
            access_log.exception("An exception occured...")
            output = b"Exception raised."

        self.write(output)
        self.finish()
#-------------------------------------------------------------------------------
# FUNCTIONS
#-------------------------------------------------------------------------------
##
## @brief      Makes an application.
##
def make_app(debug):
    return Application([
        (r"/", MainHandler)
    ], debug=debug)
#-------------------------------------------------------------------------------
# SCRIPT
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    p = ArgumentParser(add_help=True, description="DNA Decoder Server.")
    p.add_argument('-d', '--debug', action='store_true',
                   help="turns on debug mode.")
    p.add_argument('-c', '--config', default='.mkctf.yml',
                   help="mkctf configuration file.")
    args = p.parse_args()

    options.logging = 'info'
    parse_command_line(args=[])
    enable_pretty_logging()

    with open(args.config, 'r') as f:
        conf = yaml.safe_load(f)

    parameters = conf['parameters']

    AsyncIOMainLoop().install()

    app = make_app(args.debug)

    app.listen(parameters['port'])

    asyncio.get_event_loop().run_forever()
