# Other
from threading import Thread

# Commands Interfaces
from source.commands.interfaces.BalanceInterface import BalanceInterface
from source.commands.interfaces.DoubleHelpInterface import DoubleHelpInterface
from source.commands.interfaces.GlobalTopInterface import GlobalTopInterface
from source.commands.interfaces.HelpInterface import HelpInterface
from source.commands.interfaces.NoGameInterface import NoGameInterface
from source.commands.interfaces.ResetInterface import ResetInterface
from source.commands.interfaces.RussianRouletteHelpInterface import RussianRouletteHelpInterface
from source.games.interface.DoubleInterface import DoubleInterface
from source.games.interface.RussianRouletteInterface import RussianRouletteInterface
from source.static.GameInterface import GameInterface
from source.vkapi.BotAPI import BotAPI
from source.commands.interfaces.DoCInterface import DoCInterface


class CommandsHandler:
    def __init__(self, user_id, peer_id):
        self.user_id = user_id
        self.peer_id = peer_id
        self.args = None
        self.vk = BotAPI()

    def identify_comma(self, comma):
        if comma.startswith('/double'):
            new_game = Thread(target=DoubleInterface.start, args=(self.peer_id,))
            new_game.start()
        elif comma.startswith('/balance'):
            BalanceInterface.get(self.user_id, self.peer_id)
        elif '/bet' in comma:
            game = GameInterface.get_game(self.peer_id)
            if not game:
                NoGameInterface.init(self.peer_id, self.user_id)
            elif game['game'] != 'double':
                NoGameInterface.init(self.peer_id, self.user_id)
            else:
                game['interface'].bet(self.peer_id, self.user_id, comma)
        elif '/DoC' in comma and self.user_id == 239125937:
            DoCInterface.init(self.peer_id, comma)
        elif comma.startswith('/help'):
            HelpInterface.init(self.peer_id, self.user_id)
        elif comma.startswith('/reset'):
            ResetInterface.init(self.user_id, self.peer_id)
        elif comma.startswith('/doubleh'):
            DoubleHelpInterface.init(self.peer_id, self.user_id)
        elif comma.startswith('/rrh'):
            RussianRouletteHelpInterface.init(self.peer_id, self.user_id)
        elif comma.startswith('/top'):
            GlobalTopInterface.init(self.peer_id, self.user_id)
        elif comma.startswith('/rr'):
            new_game = Thread(target=RussianRouletteInterface.start, args=(self.peer_id,))
            new_game.start()
        elif comma.startswith('/rp'):
            game = GameInterface.get_game(self.peer_id)
            if not game:
                NoGameInterface.init(self.peer_id, self.user_id)
            else:
                game['interface'].add_member(self.peer_id, self.user_id)
        else:
            return
