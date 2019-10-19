import random
import time

from source.databases.UserDB import UserDB
from source.logger.LogWork import LogWork
from source.static.StaticMethods import StaticMethods


class RussianRoulette:
    def __init__(self, peer_id, game_id):
        self.number = random.randint(0, 6)
        self.peer_id = peer_id
        self.members = []
        self.game_id = game_id

    def add_member(self, user_id):

        if len(self.members) < 5:
            balance = UserDB.getter(user_id)['balance']
            UserDB.balance_changer(user_id=user_id, static_value=0)
            self.members.append({'user_id': user_id, 'value': balance, 'number': len(self.members)})
            return True
        return False

    def game(self):
        time.sleep(30)
        return self.number

    def balance_changes(self):
        if self.members:
            killed = None
            for user in self.members:
                if user['number'] == self.number:
                    killed = user

            balances_changes = []
            k = 1

            for user in self.members:
                if user['number'] != self.number:
                    UserDB.balance_changer(user_id=user['user_id'],
                                           static_value=user['value'] + killed['value'] // len(self.members))
                    changes = f"+ {killed['value'] // len(self.members)}"
                else:
                    changes = f"- {killed['value']}"
                balances_changes.append(
                    "{counter}. @id{user_id} ({name}): {changes}".format(counter=k, user_id=user['user_id'],
                                                                         changes=changes,
                                                                         name=StaticMethods.get_username(
                                                                             user['user_id']),
                                                                         ))
                k += 1
            LogWork.game_log('\n'.join(balances_changes), self.game_id)
            return balances_changes
