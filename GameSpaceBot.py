from threading import Thread

from source.console.Preview import Preview
from source.main.Main import Main
from source.vkapi.CallBackAPI import m_thread
from source.vkapi.VkAPP.GSB import app

# Preview
Preview.preview()

# Messages Handling
messages = Thread(target=Main.routine)
messages.start()

# VkApp
vk_app = Thread(target=app.run, args=('localhost', 7999, False,))
vk_app.start()

# Web Server
m_thread.run(host='localhost', port=8001, debug=False)
