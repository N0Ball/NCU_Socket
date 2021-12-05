import logging
import os
import json
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

from datetime import datetime
from pydantic import ValidationError
from modules.scheme import Com, ClientOperation

@SERVER.client()
def client_response(self, client, addr):

    try:
        msg = Com(**json.loads(self.recv(client, addr)))
        logging.debug(f"OP: {msg.OP}, DATA: {msg.DATA}")

        if msg.OP == ClientOperation.PING:
            logging.info(f"{addr[0]}:{addr[1]} tries to ping")
            self.send(client, addr, Com(OP=ClientOperation.PONG, DATA=datetime.now).dict())
            return

        if msg.OP == ClientOperation.MSG:
            logging.info(f"{addr[0]}:{addr[1]} tries to boardcast message")
            self.broadcast(json.dumps(Com(OP=ClientOperation.MSG, DATA=msg.DATA).dict()))
            return

    except ValidationError as e:
        logging.warning("Client sent an unknown type")
        logging.debug(f"Error: {e}")

if __name__ == '__main__':
    SERVER.run()