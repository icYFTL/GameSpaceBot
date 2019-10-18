import os


class ConsoleWorker:
    '''
    This class controls work with console.
    :return None
    '''

    @staticmethod
    def clear_console():
        if os.system('clear') != 0:
            os.system('cls')
