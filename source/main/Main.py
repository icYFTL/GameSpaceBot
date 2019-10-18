from Config import Config
from source.commands.CommandsHandler import CommandsHandler
from source.databases.UserDB import UserDB
from source.logger.LogWork import LogWork
from source.static.StaticData import StaticData


class Main:
    @staticmethod
    def routine():
        LogWork.log("Main routine started.")
        while True:
            StaticData.new_message_trigger.wait()
            StaticData.new_message_trigger.clear()
            data = StaticData.stack_messages.pop()

            message = data['message'].replace(f"[club{Config.group_id}|@{Config.group_short_name}]", "").strip()
            user_id = data['user_id']
            peer_id = data['peer_id']

            if message and message.strip()[0] == '/':
                if not UserDB.user_exists(user_id):
                    UserDB.add_user(user_id)
                LogWork.log("Command {message} from {user_id}".format(message=message, user_id=user_id))
                CH = CommandsHandler(user_id, peer_id)
                CH.identify_comma(message)
