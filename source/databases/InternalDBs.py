import os
import sqlite3


class InternalDBs:
    @staticmethod
    def init():
        if not os.path.exists('./database.db'):
            conn = sqlite3.connect("./database.db")
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE games
                                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        peer_id INTEGER,
                                        game_type TEXT,
                                         game_status TEXT Default "is going",
                                         data TEXT DEFAULT ""
                                        )
                                   """)
            cursor.execute("""CREATE TABLE userdata (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                       user_id INTEGER,
                                                        balance INTEGER Default 1000,
                                                        last_balance_update TEXT
                                                        )
                                                   """)
            return [conn, cursor]
        conn = sqlite3.connect("./database.db")
        cursor = conn.cursor()
        return [conn, cursor]
