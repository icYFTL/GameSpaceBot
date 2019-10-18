# Game Interfaces
from threading import Thread

# Commands Interfaces
from source.commands.interfaces.BalanceInterface import BalanceInterface
from source.commands.interfaces.GlobalTopInterface import GlobalTopInterface
from source.commands.interfaces.HelpInterface import HelpInterface
from source.commands.interfaces.NoGameInterface import NoGameInterface
from source.commands.interfaces.ResetInterface import ResetInterface
from source.games.interface.DoubleInterface import DoubleInterface
from source.static.GameInterface import GameInterface
# Static
from source.static.StaticMethods import StaticMethods
from source.vkapi.BotAPI import BotAPI


class CommandsHandler:
    def __init__(self, user_id, peer_id):
        self.user_id = user_id
        self.peer_id = peer_id
        self.args = None
        self.vk = BotAPI()

    def identify_comma(self, comma):
        if comma == '/double':
            new_game = Thread(target=DoubleInterface.start, args=(self.peer_id,))
            new_game.start()
        elif comma == '/balance':
            BalanceInterface.get(self.user_id, self.peer_id)
        elif '/bet' in comma:
            game = GameInterface.get_game(self.peer_id)
            if not game:
                NoGameInterface.init(self.peer_id, self.user_id)
            else:
                game['interface'].bet(self.peer_id, self.user_id, comma)
        elif comma == '/help':
            HelpInterface.init(self.peer_id, self.user_id)
        elif comma == '/reset':
            ResetInterface.init(self.user_id, self.peer_id)
        elif comma == '/top':
            GlobalTopInterface.init(self.peer_id, self.user_id)
        else:
            self.vk.message_send(message="@id{user_id} ({username}), нет такой команды.".format(user_id=self.user_id,
                                                                                                username=StaticMethods.get_username(
                                                                                                    self.user_id)),
                                 peer_id=self.peer_id)
