from source.static.StaticMethods import StaticMethods
from source.vkapi.BotAPI import BotAPI


class NoGameInterface:
    @staticmethod
    def init(peer_id, user_id):
        vk = BotAPI()
        vk.message_send(
            message="@id{user_id} ({username}), нет запущенных игр.\nНапишите /help для справки.".format(
                username=StaticMethods.get_username(user_id), user_id=user_id),
            peer_id=peer_id)
