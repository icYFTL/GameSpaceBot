from source.static.StaticMethods import StaticMethods
from source.vkapi.BotAPI import BotAPI


class HelpInterface:
    @staticmethod
    def init(peer_id, user_id):
        vk = BotAPI()
        vk.message_send(
            message="""@id{user_id} ({username}), пока что есть игра double.
Чтобы начать игру double - наберите /double.
Сделать ставку - /bet (количество игровой валюты) (z/r/b)

(z - Zero - Ноль - Зеленые)
(r - Red - 1:7 - Красные)
(b - Black - 8:14 - Черные)

Пример: /bet 100 z

По умолчанию - у всех новых игроков по 1000$ монет игрового баланса.

Раз в сутки можно сбрасывать свой игровой баланс командой /reset до 1000$.
Узнать глобальный топ игроков можно командой /top.
""".format(user_id=user_id, username=StaticMethods.get_username(user_id)),
            peer_id=peer_id)
