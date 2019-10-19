import time

from source.databases.GameDB import GameDB
from source.databases.UserDB import UserDB
from source.games.RussianRoulette import RussianRoulette
from source.logger.LogWork import LogWork
from source.static.GameInterface import GameInterface
from source.static.StaticData import StaticData
from source.static.StaticMethods import StaticMethods
from source.vkapi.BotAPI import BotAPI


class RussianRouletteInterface:
    @staticmethod
    def start(peer_id):
        vk = BotAPI()
        for game in StaticData.current_games:
            if game['peer_id'] == peer_id:
                vk.message_send(peer_id=peer_id, message="Игра уже началась!")
                return

        vk.message_send(message="Игра началась.\nВ течении 30 секунд вы можете заходить в игру.\nПример:(/rp)",
                        peer_id=peer_id)

        game_id = GameDB.add_game('russian_roulette', peer_id)
        game = RussianRoulette(peer_id, game_id)

        StaticData.current_games.append(
            {'game_id': game_id, 'game': 'russian_roulette', 'peer_id': peer_id, 'class': game,
             'interface': RussianRouletteInterface})

        LogWork.log("Game #{game_id} has been started at {time}".format(game_id=game_id,
                                                                        time=StaticMethods.get_time().strftime(
                                                                            "%D %T")))

        RussianRouletteInterface.end_game(peer_id, game.game())

    @staticmethod
    def end_game(peer_id, status):
        vk = BotAPI()

        current_game = GameInterface.get_game(peer_id)
        current_game['class'].game()

        GameDB.status_changer(current_game['game_id'], "post game")
        LogWork.log("Post game for Game #{game_id} has been initiated at {time}".format(game_id=current_game['game_id'],
                                                                                        time=StaticMethods.get_time().strftime(
                                                                                            '%D %T')))
        killed = None
        for user in current_game['class'].members:
            if user['number'] == status:
                killed = user
                break

        end_message = f"""Игра #{current_game['game_id']} завершена!\n@id{killed} ({StaticMethods.get_username(
            killed['user_id'])}) был убит!\nЗагаданное число: {status}."""

        vk.message_send(
            message=end_message, peer_id=peer_id)
        LogWork.game_log(end_message, current_game['game_id'])
        time.sleep(1)

        balances_changes = current_game['class'].balance_changes()

        if balances_changes:
            vk.message_send(message="Изменения балансов:\n" + '\n'.join(balances_changes), peer_id=peer_id)

        for game in range(len(StaticData.current_games)):
            if StaticData.current_games[game]['peer_id'] == peer_id:
                del (StaticData.current_games[game])

        GameDB.status_changer(current_game['game_id'], "ended")

    @staticmethod
    def add_member(peer_id, user_id):
        vk = BotAPI()

        LogWork.log(f'{user_id} trying to adding into russian_roulette')

        if UserDB.getter(user_id)['balance'] == 0:
            vk.message_send(peer_id=peer_id,
                            message="@id{user_id} ({name}), нечего ставить.".format(user_id=user_id,
                                                                                    name=StaticMethods.get_username(
                                                                                        user_id)))
            return

        for game in StaticData.current_games:
            if game['peer_id'] == peer_id:
                for user in game['class'].members:
                    if user['user_id'] == user_id:
                        vk.message_send(peer_id=peer_id,
                                        message="@id{user_id} ({name}), Вы уже в игре!".format(user_id=user_id,
                                                                                               name=StaticMethods.get_username(
                                                                                                   user_id)))
                        return

        for game in StaticData.current_games:
            if game['peer_id'] == peer_id:
                game['class'].add_member(user_id=user_id)
                vk.message_send(message="@id{user_id} ({name}), Вы в ИГРЕ!".format(user_id=user_id,
                                                                                   name=StaticMethods.get_username(
                                                                                       user_id)),
                                peer_id=peer_id)
