import traceback
import logging
import hashlib
import socket
import base64
from ..socket.server import Server
from ..header.http_headers import HTTP11, HTTPStatus

TMP_MSG=b"\x81\x05\x68\x65\x6c\x6c\x6f"

class Client:

    def __init__(self, client, host, port) -> None:
        self.CLIENT = client
        self.HOST = host
        self.PORT = port

class WebSocket:

    def __init__(self, host: str, port: int, backlog: int) -> None:
        
        self.SOCKET = Server(host, port, backlog)
        self.clients = []

        @self.SOCKET.client()
        def client_response(client, addr) -> bool:

            try:
                msg: str = str(client.recv(1024), encoding='utf-8')
                logging.info(f"Get Websocket reqest from {addr[0]}:{addr[1]}")
                logging.debug(f"MSG: {msg}")
                
                KEY = self._get_key(msg)
                ACCEPT = self._get_accept(KEY)
                RES = self._get_websocket_response(ACCEPT)

                client.send(RES)
                logging.info(f"Send to {addr[0]}:{addr[1]}")
                logging.debug(f"MSG: {str(RES)}")

                client.send(TMP_MSG)
                logging.info(f"Send to {addr[0]}:{addr[1]}")
                logging.debug(f"MSG: {TMP_MSG}")
                client.close()
                return True
            except socket.timeout:
                logging.info(f"Websocket closed because timeout")
                client.close()
                return True
            except Exception as e:
                traceback.print_exc()
                logging.error(f'Meet error: {e}')
                client.close()
                return True

    def run(self):
        self.SOCKET.run()

    def _get_key(self, header: str):
        return HTTP11(header).to_dict()['Sec-WebSocket-Key']

    def _get_accept(self, key: str) -> str:
        return create_accept(key)

    def _get_websocket_response(self, accept: str):
        res = HTTP11()
        res.setResponseHeader(
            HTTPStatus(101, 'Switching Protocols'),
            **{
                "Upgrade": "websocket",
                "Connection": "Upgrade",
                "Sec-WebSocket-Accept": accept
            }
        )
        return res.raw()

def create_accept(key: str) -> str:
    method = hashlib.sha1()
    method.update((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode('utf-8'))

    return base64.b64encode(method.digest()).decode('utf-8')

