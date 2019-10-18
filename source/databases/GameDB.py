from source.databases.InternalDBs import InternalDBs


class GameDB:
    @staticmethod
    def initialize():
        return InternalDBs.init()

    @staticmethod
    def add_game(game_type, peer_id):
        data = GameDB.initialize()
        conn, cursor = data[0], data[1]
        cursor.execute("""INSERT INTO games (game_type, peer_id)
                          VALUES ("{game_type}", {peer_id})""".format(game_type=game_type, peer_id=peer_id))
        conn.commit()
        return GameDB.get_last_id()

    @staticmethod
    def get_last_id():
        data = GameDB.initialize()
        conn, cursor = data[0], data[1]
        data = cursor.execute(
            """SELECT MAX(id) FROM games""").fetchall()
        data = list(data[0])
        return data[0]

    @staticmethod
    def getter(peer_id):
        data = GameDB.initialize()
        conn, cursor = data[0], data[1]
        data = cursor.execute(
            """SELECT * FROM games WHERE peer_id={}""".format(peer_id)).fetchall()
        data = list(data[0])
        return {'id': data[0], 'peer_id': data[1], 'game_type': data[2],
                'game_status': data[3], 'data': data[4]}

    @staticmethod
    def status_changer(game_id, status):
        data = GameDB.initialize()
        conn, cursor = data[0], data[1]
        cursor.execute(
            """UPDATE games SET game_status="{status}" WHERE id={game_id}""".format(status=status, game_id=game_id))
        conn.commit()
