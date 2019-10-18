import sys
import time

from source.console.ConsoleWorker import ConsoleWorker
from source.static.StaticData import StaticData


class Preview:
    @staticmethod
    def preview():
        ConsoleWorker.clear_console()
        print('[{}] v{}'.format(StaticData.name, StaticData.version))
        corp = 'by {}\n\n'.format(StaticData.author)

        for i in range(len(corp)):
            if corp[i].isalpha() or corp[i - 1].isalpha() and i != 0:
                sys.stdout.write(corp[i])
                sys.stdout.flush()
                time.sleep(0.2)
            else:
                sys.stdout.write(corp[i])
                sys.stdout.flush()
