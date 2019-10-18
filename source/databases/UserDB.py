from source.databases.InternalDBs import InternalDBs
from source.static.StaticMethods import StaticMethods


class UserDB:
    @staticmethod
    def initialize():
        return InternalDBs.init()

    @staticmethod
    def add_user(user_id):
        if UserDB.user_exists(user_id):
            return
        data = UserDB.initialize()
        conn, cursor = data[0], data[1]
        cursor.execute("""INSERT INTO userdata (user_id, last_balance_update)
                          VALUES ({}, "{}")""".format(user_id, StaticMethods.get_time().strftime('%D %T')))
        conn.commit()

    @staticmethod
    def get_user_by_balance(user_id):
        data = UserDB.initialize()
        conn, cursor = data[0], data[1]
        data = cursor.execute(
            """SELECT user_id,balance FROM userdata ORDER BY balance DESC""").fetchall()
        for i in range(len(data)):
            if data[i][0] == user_id:
                return [i + 1, data[i][1]]

    @staticmethod
    def get_top_balances(user_id):
        data = UserDB.initialize()
        conn, cursor = data[0], data[1]
        data = cursor.execute(
            """SELECT user_id,balance FROM userdata ORDER BY balance DESC""").fetchall()
        current_user = UserDB.get_user_by_balance(user_id)
        if data:
            top_balances = []
            for balance in data:
                top_balances.append({'user_id': balance[0], 'balance': str(balance[1]) + '$'})

            out = ""
            k = 1
            for user in top_balances:
                if k == 11:
                    out += "\n...\n"
                    out += "{counter}. @id{user_id} ({username}) - {balance}\n".format(counter=current_user[0],
                                                                                       user_id=user_id,
                                                                                       username=StaticMethods.get_username(
                                                                                           user_id),
                                                                                       balance=current_user[1])
                    break
                out += "{counter}. @id{user_id} ({username}) - {balance}\n".format(counter=k, user_id=user['user_id'],
                                                                                   username=StaticMethods.get_username(
                                                                                       user['user_id']),
                                                                                   balance=user['balance'])
                k += 1
            return out
        return False

    @staticmethod
    def change_time(user_id, time=None):
        data = UserDB.initialize()
        conn, cursor = data[0], data[1]
        cb = UserDB.getter(user_id)['balance']
        time = StaticMethods.get_time().strftime('%D %T') if not time else time
        cursor.execute(
            """UPDATE userdata SET time="{last_balance_update}" WHERE user_id={user_id}""".format(
                last_balance_update=time,
                user_id=user_id))
        conn.commit()

    @staticmethod
    def getter(user_id):
        data = UserDB.initialize()
        conn, cursor = data[0], data[1]
        data = cursor.execute(
            """SELECT * FROM userdata WHERE user_id={}""".format(user_id)).fetchall()
        data = list(data[0])
        return {'user_id': data[1], 'balance': data[2], 'last_balance_update': data[3]}

    @staticmethod
    def balance_changer(user_id, value=None, static_value=None):
        data = UserDB.initialize()
        conn, cursor = data[0], data[1]
        cb = UserDB.getter(user_id)['balance']
        cursor.execute(
            """UPDATE userdata SET balance={balance} WHERE user_id={user_id}""".format(
                balance=cb + value if value else static_value,
                user_id=user_id))
        conn.commit()

    @staticmethod
    def user_exists(user_id):
        data = UserDB.initialize()
        conn, cursor = data[0], data[1]
        if cursor.execute("""SELECT * FROM userdata WHERE user_id={}""".format(user_id)).fetchall():
            return True
        return False
