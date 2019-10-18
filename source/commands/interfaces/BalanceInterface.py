from source.databases.UserDB import UserDB
from source.static.StaticMethods import StaticMethods
from source.vkapi.BotAPI import BotAPI


class BalanceInterface:
    @staticmethod
    def get(user_id, peer_id):
        vk = BotAPI()
        vk.message_send(
            message="@id{user_id} ({username}), ваш баланс: {balance}$".format(
                username=StaticMethods.get_username(user_id),
                balance=UserDB.getter(user_id)['balance'], user_id=user_id),
            peer_id=peer_id)
