import traceback
import logging
import hashlib
import socket
import base64
from typing import ByteString
from ..socket.server import Server
from ..header.http_headers import HTTP11, HTTPStatus

class Client:

    def __init__(self, client, host, port) -> None:
        self.CLIENT = client
        self.HOST = host
        self.PORT = port

class _WebSocket:

    def __init__(self):
        self.CLIENTS = []
    
    def _get_key(self, header: str) -> str:
        return HTTP11(header).to_dict()['Sec-WebSocket-Key']

    def _get_accept(self, key: str) -> str:
        method = hashlib.sha1()
        method.update((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode('utf-8'))

        return base64.b64encode(method.digest()).decode('utf-8')

    def _get_websocket_response(self, accept: str) -> ByteString:
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

    def _check_register(self, host: str, port: int, client: socket) -> bool:

        for client in self.CLIENTS:
            
            if client.HOST == host and client.PORT == port:
                return True

        self.CLIENTS.push(Client(client, host, port))
        return False

    def _register(self, client, addr):
        msg: str = str(client.recv(1024), encoding='utf-8')
        logging.info(f"Get Websocket reqest from {addr[0]}:{addr[1]}")
        logging.debug(f"MSG: {msg}")
        
        KEY = self._get_key(msg)
        ACCEPT = self._get_accept(KEY)
        RES = self._get_websocket_response(ACCEPT)

        client.send(RES)
        logging.info(f"Send to {addr[0]}:{addr[1]}")
        logging.debug(f"MSG: {str(RES)}")

    def _serve(self, client, addr):
        data = "NAN"
        self.serv_func(data)

class WebSocket(_WebSocket):

    def __init__(self, host: str, port: int, backlog: int) -> None:
        super.__init__()
        self.SOCKET = Server(host, port, backlog)

        @self.SOCKET.client()
        def client_response(client, addr) -> bool:

            try:

                self._register(client, addr) if not self._check_register(addr[0], addr[1], client) else self._serve(client, addr)

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