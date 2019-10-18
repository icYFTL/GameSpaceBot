import random

import vk_api

from Config import Config


class BotAPI:
    def __init__(self):
        self.vk = vk_api.VkApi(token=Config.group_vk_access_token)

    def message_send(self, peer_id, message=None, attach=None):
        self.vk.method("messages.send",
                       {'peer_id': peer_id, 'message': message, 'random_id': random.randint(0, 100000),
                        'attachment': attach})

    def get_chat_members(self, peer_id):
        pass
