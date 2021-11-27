import os
MODE = os.getenv('MODE')

from config import getModeConfig

CONFIG = getModeConfig(MODE)

import coloredlogs, logging

if CONFIG.MODE == "DEBUG":
    coloredlogs.install(level='DEBUG')
else:
    coloredlogs.install(level='INFO')

from modules.websocket.server import WebSocket
SERVER = WebSocket(CONFIG.HOST, CONFIG.PORT, CONFIG.BACKLOG)

if __name__ == '__main__':
    SERVER.run()