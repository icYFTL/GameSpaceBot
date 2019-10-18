import time

from source.databases.GameDB import GameDB
from source.databases.UserDB import UserDB
from source.games.Double import Double
from source.logger.LogWork import LogWork
from source.static.GameInterface import GameInterface
from source.static.StaticData import StaticData
from source.static.StaticMethods import StaticMethods
from source.vkapi.BotAPI import BotAPI


class DoubleInterface:
    @staticmethod
    def start(peer_id):
        vk = BotAPI()
        for game in StaticData.current_games:
            if game['peer_id'] == peer_id:
                vk.message_send(peer_id=peer_id, message="Игра уже началась!")
                return

        vk.message_send(message="Игра началась.\nВ течении 60 секунд вы можете ставить.\nПример:(/bet 100 z)",
                        peer_id=peer_id)
        game = Double(peer_id)
        game_id = GameDB.add_game('double', peer_id)
        StaticData.current_games.append(
            {'game_id': game_id, 'game': 'double', 'peer_id': peer_id, 'class': game,
             'interface': DoubleInterface})
        LogWork.log("Game #{game_id} has been started at {time}".format(game_id=game_id,
                                                                        time=StaticMethods.get_time().strftime(
                                                                            "%D %T")))
        DoubleInterface.end_game(peer_id)

    @staticmethod
    def get_args_bet(comma):
        try:
            args = {}
            comma = comma.split()[1::]
            for i in comma:
                if i == 'z' or i == 'r' or i == 'b':
                    args.update({'bet': i})
                try:
                    args.update({'value': int(i)})
                except:
                    pass
            if len(args.keys()) > 1:
                return args
            return False
        except:
            return False

    @staticmethod
    def bet(peer_id, user_id, comma):
        LogWork.log("{user_id} trying to bet like {comma}".format(user_id=user_id, comma=comma))
        vk = BotAPI()

        comma = DoubleInterface.get_args_bet(comma)

        if not comma:
            vk.message_send(
                message="@id{user_id} ({name}), неверно указана ставка.".format(user_id=user_id,
                                                                                name=StaticMethods.get_username(
                                                                                    user_id)),
                peer_id=peer_id)
            return

        value, bet = comma['value'], comma['bet']

        if not UserDB.user_exists(user_id):
            UserDB.add_user(user_id)

        balance = UserDB.getter(user_id)['balance']

        if balance < value:
            vk.message_send(
                message="@id{user_id} ({name}), у Вас недостаточно средств.".format(user_id=user_id,
                                                                                    name=StaticMethods.get_username(
                                                                                        user_id)),
                peer_id=peer_id)
            return

        if value < 0:
            value *= -1

        for game in StaticData.current_games:
            if game['peer_id'] == peer_id:
                for user in game['class'].bets:
                    if user['user_id'] == user_id:
                        vk.message_send(peer_id=peer_id,
                                        message="@id{user_id} ({name}), вы уже сделали ставку!".format(user_id=user_id,
                                                                                                       name=StaticMethods.get_username(
                                                                                                           user_id)))
                        return

        for game in StaticData.current_games:
            if game['peer_id'] == peer_id:
                game['class'].bet(value=value, user_id=user_id, bet=bet)
                vk.message_send(message="@id{user_id} ({name}), Ваша ставка принята!".format(user_id=user_id,
                                                                                             name=StaticMethods.get_username(
                                                                                                 user_id)),
                                peer_id=peer_id)

    @staticmethod
    def pic_switcher(number):
        if number == 0:
            return "doc239125937_511378630"
        elif number == 1:
            return "doc239125937_511378656"
        elif number == 2:
            return "doc239125937_511378667"
        elif number == 3:
            return "doc239125937_511378671"
        elif number == 4:
            return "doc239125937_511378674"
        elif number == 5:
            return "doc239125937_511378678"
        elif number == 6:
            return "doc239125937_511378682"
        elif number == 7:
            return "doc239125937_511378686"
        elif number == 8:
            return "doc239125937_511378689"
        elif number == 9:
            return "doc239125937_511378695"
        elif number == 10:
            return "doc239125937_511378702"
        elif number == 11:
            return "doc239125937_511378715"
        elif number == 12:
            return "doc239125937_511378720"
        elif number == 13:
            return "doc239125937_511378723"
        elif number == 14:
            return "doc239125937_511378728"

    @staticmethod
    def end_game(peer_id):
        vk = BotAPI()

        current_game = GameInterface.get_game(peer_id)
        current_game['class'].init()

        GameDB.status_changer(current_game['game_id'], "post game")
        LogWork.log("Post game for Game #{game_id} has been initiated at {time}".format(game_id=current_game['game_id'],
                                                                                        time=StaticMethods.get_time().strftime(
                                                                                            '%D %T')))
        status = current_game['class'].get_status()

        vk.message_send(attach=DoubleInterface.pic_switcher(status['number']), peer_id=peer_id)

        time.sleep(20)

        vk.message_send(
            message="Игра #{game_id} завершена!\n{team} победили!\nЗагаданное число: {number}.".format(
                game_id=current_game['game_id'],
                number=status['number'], team=status['won']), peer_id=peer_id)

        time.sleep(1)

        balances_changes = current_game['class'].balance_changes()

        if balances_changes:
            vk.message_send(message="Изменения балансов:\n" + '\n'.join(balances_changes), peer_id=peer_id)

        for game in range(len(StaticData.current_games)):
            if StaticData.current_games[game]['peer_id'] == peer_id:
                del (StaticData.current_games[game])

        GameDB.status_changer(current_game['game_id'], "ended")
