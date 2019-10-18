from source.static.StaticData import StaticData


class GameInterface:
    @staticmethod
    def get_game(peer_id):
        for game in StaticData.current_games:
            if game['peer_id'] == peer_id:
                return game
        return False
