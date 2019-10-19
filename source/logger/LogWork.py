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
        try:
            os.mkdir("source/logger/logs/game_logs/")
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

    @staticmethod
    def game_log(message, game_id):
        LogWork.base_init()
        f = open(f'source/logger/logs/game_logs/{game_id}.txt', 'a', encoding='utf-8')
        f.write(message)
        f.close()
