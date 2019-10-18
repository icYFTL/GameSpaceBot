from source.databases.UserDB import UserDB
from source.vkapi.BotAPI import BotAPI


class GlobalTopInterface:
    @staticmethod
    def init(peer_id, user_id):
        vk = BotAPI()
        vk.message_send(
            message="""Глобальный топ:
{global_top}
""".format(global_top=UserDB.get_top_balances(user_id)),
            peer_id=peer_id)
