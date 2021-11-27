import os
MODE = os.getenv('MODE')

from config import getModeConfig

MODE = getModeConfig(MODE)()

import coloredlogs, logging
coloredlogs.install()

FORMAT = '%(asctime)s %(levelname)s: %(message)s'

if MODE['MODE'] == "DEBUG":
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
else:
    logging.basicConfig(level=logging.INFO, format=FORMAT)

from modules.socket import Server

if __name__ == '__main__':
    server = Server(MODE["HOST"], MODE["PORT"], MODE["BACKLOG"])
    SERVER = server.run()