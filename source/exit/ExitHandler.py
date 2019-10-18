import atexit

from source.logger.LogWork import LogWork


class ExitHandler:
    @staticmethod
    def init():
        atexit.register(ExitHandler.handler())

    @staticmethod
    def handler():
        LogWork.warn("Script is downing now...")
