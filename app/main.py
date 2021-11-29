import os
MODE = os.getenv('MODE')

from config import getModeConfig

CONFIG = getModeConfig(MODE)

import coloredlogs

if CONFIG.MODE == "DEBUG":
    coloredlogs.install(level='DEBUG')
else:
    coloredlogs.install(level='INFO')

from modules.websocket.server import WebSocket
SERVER = WebSocket(CONFIG.HOST, CONFIG.PORT, CONFIG.BACKLOG)

@SERVER.client()
def client_response(self, client, addr):

    self.send(client, addr, "Hello!")
    msg = self.recv(client, addr)
    self.broadcast(msg)

    # client.close()

if __name__ == '__main__':
    SERVER.run()