import logging
import os

import hues


class LogWork:
    @staticmethod
    def base_init():
        try:
            os.mkdir("source/logger/logs/")
        except:
            pass
        logging.basicConfig(filename="source/logger/logs/default.log", level=logging.INFO)

    @staticmethod
    def log(message):
        LogWork.base_init()
        logging.info(message)
        hues.log(message)

    @staticmethod
    def warn(message):
        LogWork.base_init()
        logging.warning(message)
        hues.warn(message)

    @staticmethod
    def error(message):
        LogWork.base_init()
        logging.error(message)
        hues.error(message)

    @staticmethod
    def fatal(message):
        LogWork.base_init()
        logging.fatal(message)
        hues.error("Fatal: " + message)
