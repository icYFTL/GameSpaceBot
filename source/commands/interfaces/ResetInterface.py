from datetime import datetime
from time import strptime, mktime

from source.databases.UserDB import UserDB
from source.static.StaticMethods import StaticMethods
from source.vkapi.BotAPI import BotAPI


class ResetInterface:
    @staticmethod
    def init(user_id, peer_id):
        vk = BotAPI()
        user = UserDB.getter(user_id)

        current_time = strptime(StaticMethods.get_time().strftime('%D %T'), '%m/%d/%y %H:%M:%S')
        last_time = strptime(user['last_balance_update'], '%m/%d/%y %H:%M:%S')

        current_time = datetime.fromtimestamp(mktime(current_time))
        last_time = datetime.fromtimestamp(mktime(last_time))

        delta = str(last_time - current_time).split(',')[1].strip()

        if (current_time - last_time).days < 1:
            vk.message_send(
                message="@id{user_id} ({username}), до ресета нужно подождать еще {time}".format(user_id=user_id,
                                                                                                 time=delta,
                                                                                                 username=StaticMethods.get_username(
                                                                                                     user_id)),
                peer_id=peer_id)
        elif user['balance'] >= 1000:
            vk.message_send(
                message="@id{user_id} ({username}), в текущий момент у Вас на балансе {balance}. Делать ресет баланса бесполезно.".format(
                    user_id=user_id,
                    balance=user['balance'],
                    username=StaticMethods.get_username(user_id)),
                peer_id=peer_id)
        else:
            UserDB.balance_changer(user_id=user_id, static_value=1000)
            vk.message_send(
                message="@id{user_id} ({username}), баланс успешно сброшен до 1000$.".format(
                    user_id=user_id, username=StaticMethods.get_username(user_id)),
                peer_id=peer_id)
            UserDB.change_time(user_id=user_id)
