import os
MODE = os.getenv('MODE')

from config import getModeConfig

CONFIG = getModeConfig(MODE)

import coloredlogs, logging

if CONFIG.MODE == "DEBUG":
    coloredlogs.install(level='DEBUG')
else:
    coloredlogs.install(level='INFO')

from modules.socket import Server
SERVER = Server(CONFIG.HOST, CONFIG.PORT, CONFIG.BACKLOG)

@SERVER.client()
def client_response(client, addr):
    msg: str = str(client.recv(1024), encoding='utf-8')[:-1]
    logging.info(f"Recved message from {addr[0]}:{addr[1]}")
    logging.debug(f'MSG: {msg}')

    if msg == "exit":
        logging.info(f'{addr[0]}:{addr[1]} disconnected')
        client.close()
        return False
    elif msg:
        logging.info(f"Sending message to {addr[0]}:{addr[1]}")
        logging.debug(f"MSG: {msg.upper()}")
        send_msg = msg.upper() + '\r\n'
        client.send(send_msg.encode('utf-8'))
    else:
        raise Exception("Something's wrong")

if __name__ == '__main__':
    SERVER.run()