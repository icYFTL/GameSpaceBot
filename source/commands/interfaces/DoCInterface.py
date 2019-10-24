from source.static.StaticMethods import StaticMethods
from source.static.StaticData import StaticData
from source.vkapi.BotAPI import BotAPI

import random


class DoCInterface:
    @staticmethod
    def get_args(comma):
        try:
            args = {}
            comma = comma.split()[1::]
            for i in comma:
                if i == 'z' or i == 'r' or i == 'b':
                    args.update({'type': i})
                try:
                    if int(i) > 0:
                        args.update({'id': int(i)})
                except:
                    pass
            if len(args.keys()) > 1:
                return args
            return False
        except:
            return False

    @staticmethod
    def init(peer_id, comma):
        vk = BotAPI()
        args = DoCInterface.get_args(comma)
        for i in range(len(StaticData.current_games)):
            if StaticData.current_games[i]['game_id'] == args['id'] and StaticData.current_games[i]['game'] == 'double':
                if args['type'] == 'r':
                    StaticData.current_games[i]['class'].number = random.randint(1, 7)
                elif args['type'] == 'b':
                    StaticData.current_games[i]['class'].number = random.randint(8, 14)
                elif args['type'] == 'z':
                    StaticData.current_games[i]['class'].number = 0
        vk.message_send(peer_id=peer_id, message="Шалость удалась.")
