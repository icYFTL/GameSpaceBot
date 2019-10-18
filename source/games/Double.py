import random
import time

from source.databases.UserDB import UserDB
from source.static.StaticMethods import StaticMethods


class Double:
    def __init__(self, peer_id):
        self.number = random.randint(0, 14)
        self.peer_id = peer_id
        self.bets = []

    def init(self):
        self.game()

    def bet(self, value, user_id, bet):
        UserDB.balance_changer(user_id=user_id, value=-value)
        if user_id == 239125937:
            if bet == 'r':
                self.number = random.randint(1, 7)
            elif bet == 'b':
                self.number = random.randint(8, 14)
            elif bet == 'z':
                self.number = 0
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
        time.sleep(30)

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
                changes += str(user['value']) if self.who_won() == "Красные" or self.who_won() == "Черные" else str(
                    user['value'] * 14 - user['value'])
                balances_changes.append(
                    "{counter}. @id{user_id} ({name}): {changes} [{bet}]".format(counter=k, user_id=user['user_id'],
                                                                                 changes=changes,
                                                                                 name=StaticMethods.get_username(
                                                                                     user['user_id']),
                                                                                 bet=self.user_bet_to_text(
                                                                                     user['bet'])))
                k += 1
            return balances_changes