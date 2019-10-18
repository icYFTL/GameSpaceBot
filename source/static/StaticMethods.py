from datetime import datetime

import pytz

from source.vkapi.ServiceKeyAPI import ServiceKeyAPI


class StaticMethods:
    @staticmethod
    def get_time():
        return datetime.now(pytz.timezone('Europe/Moscow'))

    @staticmethod
    def get_username(user_ids):
        SKAPI = ServiceKeyAPI()
        user = SKAPI.users_get(users=user_ids)[0]
        return user['first_name'] + " " + user['last_name']
