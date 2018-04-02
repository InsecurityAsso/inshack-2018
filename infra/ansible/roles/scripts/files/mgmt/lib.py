import configparser
import logging

LOG_FILE = "./scripts.log"
LOG_LEVEL = logging.INFO
CONF_FILE = "./scripts.conf"

class Script:
    def __init__(self):
        self.init_config()
        self.init_logger()

    def init_config(self):
        self.config = configparser.ConfigParser()
        self.config.read(CONF_FILE)

    def init_logger(self):
        logger = logging.getLogger()

        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%FT%T"
        )

        handlers = [
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(LOG_FILE),
        ]

        for handler in handlers:
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        logger.setLevel(LOG_LEVEL)

        self.logger = logger
