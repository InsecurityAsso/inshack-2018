#!/usr/bin/env python3
# -!- encoding:utf-8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: dna_decoder_wrapper.py
#    date: 2017-08-30
#  author: paul.dautry
# purpose:
#      Wrapper for virtual printer script
# license:
#      GPLv3
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
#==============================================================================
import asyncio
import aioredis
from ruamel import yaml
from argparse import ArgumentParser
from tornado.web import Application, RequestHandler
from tornado.log import access_log, enable_pretty_logging
from tornado.options import options, parse_command_line
from virtual_printer import print_img
from tornado.platform.asyncio import AsyncIOMainLoop
#==============================================================================
# CONFIG
#==============================================================================
REDIS_TIMEOUT = 5.0 # seconds
#==============================================================================
# CLASSES
#==============================================================================
##
## @brief      Class for main handler.
##
class MainHandler(RequestHandler):
    ##
    ## @brief      { function_description }
    ##
    def get(self):
        self.write(b"""
<html>
    <head>
        <title>Virtual Printer Service</title>
        <link rel="icon" type="image/gif" href="data:image/gif;base64,R0lGODlhEAAQAIAAAAAAAAAAACH5BAkAAAEALAAAAAAQABAAAAIgjI+py+0PEQiT1lkNpppnz4HfdoEH2W1nCJRfBMfyfBQAOw==">
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
|   > /print: expects data to be a PNG file (RGB or RGBA).                     |
|   < you'll get your A4 page printed in the response as raw PNG data.         |
|                                                                              |
|   $> curl -X POST --form "f=@<file.png>" <url>                               |
|                                                                              |
|   > /serial-number: expects data to be a base64 encoded S/N                  |
|   < you'll get the flag if you're right                                      |
|                                                                              |
|   $> curl -X POST --data "sn=<b64encoded-serial-number>" <url>               |
|                                                                              |
+------------------------------------------------------------------------------+
        </pre>
        <pre style="visibility: hidden;">
            If y0u w4nn4 l34k, b3 sm4rt & st34lthy.
        </pre>
        <pre style="visibility: hidden;">
            Tested with curl 7.55.1
        </pre>
    </body>
</html>
""")
##
## @brief      Class for print handler.
##
class PrintHandler(RequestHandler):
    ##
    ## @brief      { function_description }
    ##
    def initialize(self, redis_host, redis_port):
        self.redis_addr = (redis_host, redis_port)
    ##
    ## @brief      { function_description }
    ##
    def __reject(self, reason):
        self.set_status(400)    # I'm a teapot
        self.write({'reason': reason})
        self.finish()
    ##
    ## @brief      { function_description }
    ##
    def __accept(self, data):
        if isinstance(data, str):
            data = data.encode()
        self.write(data)
        self.finish()
    ##
    ## @brief      Saves a secret.
    ##
    async def __save_secret(self, secret):
        key = 'vps-' + self.request.remote_ip
        redis = await aioredis.create_redis(self.redis_addr, timeout=REDIS_TIMEOUT)
        access_log.info('adding: ({}, {})'.format(key, secret))
        await redis.set(key, secret, expire=30) # register secret
        redis.close()
    ##
    ## @brief      { function_description }
    ##
    async def __print(self):
        files = self.request.files['f']

        if len(files) != 1:
            self.__reject("/print expects exactly one image file.")
            return

        img_data = files[0]['body']

        try:
            result = print_img(img_data, self.request.remote_ip)
        except Exception as e:
            access_log.exception("An exception occurred...")
            self.__reject("[print_img:exception] service failed to process "
                          "your image. Try with another one.\nIf the problem "
                          "persists with other images, please contact an "
                          "admin.")
            return

        if not result['status']:
            self.__reject(result['error'])
            return

        page_data = result['data']
        secret = result['b64sn']

        try:
            await self.__save_secret(secret)
        except Exception as e:
            access_log.exception("An exception occurred...")
            self.__reject("[__save_secret:exception] service failed to save "
                          "the secret. Request timed-out.\nPlease contact an "
                          "admin. Redis server might be down.")
            return

        self.__accept(page_data)
    ##
    ## @brief      { function_description }
    ##
    async def post(self):
        await self.__print()
##
## @brief      Class for serial number handler.
##
class SerialNumberHandler(RequestHandler):
    ##
    ## @brief      { function_description }
    ##
    def initialize(self, redis_host, redis_port, flag):
        self.redis_addr = (redis_host, redis_port)
        self.flag = flag
    ##
    ## @brief      { function_description }
    ##
    def __reject(self, reason):
        self.set_status(400)    # I'm a teapot
        self.write({'reason': reason})
        self.finish()
    ##
    ## @brief      { function_description }
    ##
    def __accept(self, data):
        if isinstance(data, str):
            data = data.encode()
        self.write(data)
        self.finish()
    ##
    ## @brief      Loads a secret.
    ##
    async def __load_secret(self):
        key = 'vps-' + self.request.remote_ip
        redis = await aioredis.create_redis(self.redis_addr, timeout=REDIS_TIMEOUT)
        secret = await redis.get(key)
        redis.close()
        access_log.info('retrieving: ({}, {})'.format(key, secret))
        return secret
    ##
    ## @brief      { function_description }
    ##
    async def __serial_number(self):
        data = self.request.body

        if data[0:3] == b'sn=':
            secret = data[3:]

            try:
                saved_secret = await self.__load_secret()
            except Exception as e:
                self.__reject("[__load_secret:exception] service failed to "
                              "save the secret. Request timed-out.\nPlease "
                              "contact an admin. Redis server might be down.")
                return

            if saved_secret is None:
                self.__reject("Too late, you must submit your serial-number "
                              "within a timeframe of 25 seconds after your "
                              "image was printed.")
                return

            if secret == saved_secret:
                access_log.info("{} gets a flag!".format(self.request.remote_ip))
                self.__accept("Good job ! DO NOT LEAK SECRET FILES BY "
                              "PRINTING THEM ! You can validate with: "
                              "{}".format(self.flag))
                return

            self.__reject("Wrong secret... Try again :)")
            return

        self.__reject("could not find the serial number.\nPlease upload data "
                      "using the following command: curl -d "
                      "'sn=<b64encoded_serial_number>' "
                      "http://...:.../serial-number")
        return
    ##
    ## @brief      { function_description }
    ##
    async def post(self):
        await self.__serial_number()
#===============================================================================
# FUNCTIONS
#===============================================================================
##
## @brief      Makes an application.
##
def make_app(redis_host, redis_port, flag, debug):
    return Application([
        (r"/", MainHandler),
        (r"/print", PrintHandler, dict(redis_host=redis_host,
                                       redis_port=redis_port)),
        (r"/serial-number", SerialNumberHandler, dict(redis_host=redis_host,
                                                      redis_port=redis_port,
                                                      flag=flag))
    ], debug=debug)
#===============================================================================
# SCRIPT
#===============================================================================
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

    app = make_app(parameters['server']['redis-host'],
                   parameters['server']['redis-port'],
                   conf['flag'],
                   args.debug)

    app.listen(parameters['port'])

    asyncio.get_event_loop().run_forever()
