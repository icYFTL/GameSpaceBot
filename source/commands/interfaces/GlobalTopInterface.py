from source.databases.UserDB import UserDB
from source.static.StaticMethods import StaticMethods
from source.vkapi.BotAPI import BotAPI


class GlobalTopInterface:
    @staticmethod
    def init(peer_id, user_id):
        vk = BotAPI()
        data = UserDB.get_top_balances()
        current_user = UserDB.get_user_by_balance(user_id)
        if data:
            top_balances = []
            for balance in data:
                top_balances.append({'user_id': balance[0], 'balance': str(balance[1]) + '$'})

            out = ""
            k = 1
            done = False
            for user in top_balances:
                if k == 6 and not done:
                    out += "...\n"
                    out += "{counter}. @id{user_id} ({username}) - {balance}$\n".format(counter=current_user[0],
                                                                                        user_id=user_id,
                                                                                        username=StaticMethods.get_username(
                                                                                            user_id),
                                                                                        balance=current_user[1])
                    break
                elif k == 6:
                    break
                if user['user_id'] == user_id:
                    done = True
                out += "{counter}. @id{user_id} ({username}) - {balance}\n".format(counter=k, user_id=user['user_id'],
                                                                                   username=StaticMethods.get_username(
                                                                                       user['user_id']),
                                                                                   balance=user['balance'])
                k += 1
            try:
                vk.message_send(
                    message=f'Глобальный топ:\n{out}',
                    peer_id=peer_id)
            except:
                pass
