from threading import Thread

from source.console.Preview import Preview
from source.main.Main import Main
from source.vkapi.CallBackAPI import m_thread

# Preview
Preview.preview()

# Messages Handling
messages = Thread(target=Main.routine)
messages.start()

# Web Server
m_thread.run(host='localhost', port=8001, debug=False)
