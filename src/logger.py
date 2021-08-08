#!/usr/bin/python3

import logging

from logging.handlers import TimedRotatingFileHandler
from src.singleton import Singleton


class Logger(Singleton):

    LOGS_PATH = 'logs/obb.log'

    def __init__(self):

        self.logger = logging.getLogger('logger')
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s - %(process)d - %(levelname)s - %(message)s')
        handler = TimedRotatingFileHandler(self.LOGS_PATH,
                                           when="midnight",
                                           interval=1)
        handler.suffix = "%Y%m%d"
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        cformatter = logging.Formatter(
            '%(asctime)s - %(process)d - %(levelname)s - %(message)s')
        chandler = logging.StreamHandler()
        chandler.setLevel(logging.INFO)
        chandler.setFormatter(cformatter)
        self.logger.addHandler(chandler)

    def debug(self, message):
        self.logger.debug(message)

    def error(self, message):
        self.logger.error(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def critical(self, message):
        self.logger.critical(message)
