import random
import time

from source.databases.UserDB import UserDB
from source.logger.LogWork import LogWork
from source.static.StaticMethods import StaticMethods


class Double:
    def __init__(self, peer_id, game_id):
        self.number = random.randint(0, 14)
        self.peer_id = peer_id
        self.bets = []
        self.game_id = game_id

    def bet(self, value, user_id, bet):
        UserDB.balance_changer(user_id=user_id, value=-value)
        self.bets.append({'user_id': user_id, 'value': value, 'bet': bet})

    def user_bet_to_text(self, bet):
        if bet == 'r':
            return "Красные"
        elif bet == 'b':
            return "Черные"
        else:
            return "Зеленые"

    def who_won(self):
        if self.number == 0:
            return "Зеленые"
        elif self.number < 8:
            return "Красные"
        else:
            return "Черные"

    def won(self, bet):
        won = self.who_won()
        if bet == 'r' and won == "Красные":
            return True
        elif bet == 'b' and won == "Черные":
            return True
        elif bet == 'z' and won == "Зеленые":
            return True
        else:
            return False

    def get_status(self):
        return {'number': self.number, 'bets': self.bets, 'won': self.who_won()}

    def game(self):
        time.sleep(60)

    def balance_changes(self):
        if self.bets:
            for bet in self.bets:
                if (bet['bet'] == 'r' or bet['bet'] == 'b') and self.won(bet['bet']):
                    UserDB.balance_changer(user_id=bet['user_id'], value=bet['value'] * 2)
                elif bet['bet'] == 'z' and self.won(bet['bet']):
                    UserDB.balance_changer(user_id=bet['user_id'], value=bet['value'] * 14)
            balances_changes = []
            k = 1
            for user in self.bets:
                changes = "+" if self.won(user['bet']) else "-"
                changes += str(user['value'])
                balances_changes.append(
                    "{counter}. @id{user_id} ({name}): {changes} [{bet}]".format(counter=k, user_id=user['user_id'],
                                                                                 changes=changes,
                                                                                 name=StaticMethods.get_username(
                                                                                     user['user_id']),
                                                                                 bet=self.user_bet_to_text(
                                                                                     user['bet'])))
                k += 1
            LogWork.game_log('\n'.join(balances_changes), self.game_id)
            return balances_changes
