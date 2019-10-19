from source.static.StaticMethods import StaticMethods
from source.vkapi.BotAPI import BotAPI


class RussianRouletteHelpInterface:
    @staticmethod
    def init(peer_id, user_id):
        vk = BotAPI()
        vk.message_send(
            message="""@id{user_id} ({username}),
Чтобы начать игру Russian Roulette - наберите /rr.
Принять участие - /rp

• 1 патрон в 6 ячейках револьвера.
• Каждый игрок идет вабанк.
• В случае проигрыша - деньги проигравшего деляться на всех поровну.
""".format(user_id=user_id, username=StaticMethods.get_username(user_id)),
            peer_id=peer_id)
