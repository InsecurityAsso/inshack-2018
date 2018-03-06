#!/usr/bin/env python3
# -!- encoding:utf8 -!-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: server.py
#     date: 2018-03-04
#   author: paul.dautry
#  purpose:
#       /!\ FOR EDUCATIONAL PURPOSE ONLY /!\
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  IMPORTS
# =============================================================================
import os
import json
import asyncio
from ruamel import yaml
from pprint import pprint
from argparse import ArgumentParser
from tornado.web import Application, RequestHandler
from tornado.log import access_log, enable_pretty_logging
from urllib.parse import urlparse, parse_qs
from tornado.options import options, parse_command_line
from tornado.platform.asyncio import AsyncIOMainLoop
# =============================================================================
#  CONSTANTS
# =============================================================================
COOKIE_KEY = 'uuid'
# =============================================================================
#  CLASSES
# =============================================================================
##
## @brief      Class for main handler.
##
class MainHandler(RequestHandler):
    ##
    ## @brief      { function_description }
    ##
    def get(self):
        self.write("""

     . .  .  .  . . .
.                     .                  _.-/`/`'-._
. Why are you here ?  .                /_..--''''_-'
    .  .  .  .      .`                //-.__\_\.-'
                `..'  _\\\//  --.___ // ___.---.._
                  _- /@/@\  \       ||``          `-_
                .'  ,\_\_/   |    \_||_/      ,-._   `.
               ;   { o    /   }     ""        `-._`.   ;
              ;     `-==-'   /                    \_|   ;
             |        |>o<|  }@@@}                       |
             |       <(___<) }@@@@}                      |
             |       <(___<) }@@@@@}                     |
             |        <\___<) \_.?@@}                    |
              ;         V`--V`__./@}                    ;
               \      tx      ooo@}                    /
                \                                     /
                 `.                                 .'
                   `-._                         _.-'ls
                       ``------'''''''''------``

""")
##
## @brief      Class for notify handler.
##
class NotifyHandler(RequestHandler):
    ##
    ## @brief      { function_description }
    ##
    def post(self):
        try:
            payload = json.loads(self.request.body.decode())
        except Exception as e:
            self.set_status(403)
            self.write({'exception': repr(e)})
            return

        print("payload from {}".format(self.request.remote_ip))
        pprint(payload)

        uuid = payload.get('uuid')
        if uuid is None:
            self.set_status(400)
            self.write({'error': 'missing uuid in payload.'})
            return

        cookie = '{}[{}]'.format(uuid, self.request.remote_ip)

        self.set_secure_cookie(COOKIE_KEY, cookie)
        self.write("thank you very much :)")
##
## @brief      Class for flag handler.
##
class FlagHandler(RequestHandler):
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
        parsed = urlparse(self.request.uri)
        params = parse_qs(parsed.query)

        uuid = params.get('uuid')
        if uuid is None:
            self.write("give me your uuid man... :/")
            return

        cookie = self.get_secure_cookie(COOKIE_KEY)
        if not cookie:
            self.write("your cookie missing or maybe you don't know what HMAC"
                       " means :(")
            return

        try:
            cookie = cookie.decode()
        except Exception as e:
            access_log.exception("An exception occured...")
            self.write("why did you change your cookie...")
            return

        expected_cookie = '{}[{}]'.format(uuid[0], self.request.remote_ip)

        if cookie != expected_cookie:
            self.write("you're almost done... i got a uuid and a cookie... "
                       "but they don't match.")
            return

        self.write("here is your reward my dear: {}".format(self.flag))
# =============================================================================
#  FUNCTIONS
# =============================================================================
##
## @brief      Makes an application.
##
def make_app(flag, debug):
    return Application([
        (r"/", MainHandler),
        (r"/notify", NotifyHandler),
        (r"/flag", FlagHandler, dict(flag=flag))
    ],
    debug=debug,
    cookie_secret=os.urandom(32).hex())
# =============================================================================
#  SCRIPT
# =============================================================================
if __name__ == "__main__":
    p = ArgumentParser(add_help=True, description="Virtual Printer Server.")
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

    app = make_app(conf['flag'],
                   args.debug)

    app.listen(parameters['port'])

    asyncio.get_event_loop().run_forever()
