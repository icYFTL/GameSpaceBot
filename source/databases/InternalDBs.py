import sqlite3


class InternalDBs:
    @staticmethod
    def init():
        conn = sqlite3.connect("./database.db")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS games
                                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    peer_id INTEGER,
                                    game_type TEXT,
                                     game_status TEXT Default "is going",
                                     data TEXT DEFAULT ""
                                    )
                               """)
        cursor.execute("""CREATE TABLE IF NOT EXISTS userdata (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                   user_id INTEGER,
                                                    balance INTEGER Default 1000,
                                                    last_balance_update TEXT,
                                                    conservations TEXT
                                                    )
                                               """)
        return [conn, cursor]
