import vk_api

from Config import Config


class ServiceKeyAPI:
    def __init__(self):
        self.vk = vk_api.VkApi(token=Config.service_key)

    def users_get(self, users):
        return self.vk.method("users.get", {"user_ids": users})
