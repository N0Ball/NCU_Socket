import traceback
import logging
import hashlib
import socket
import base64
from typing import ByteString
from ..socket.server import Server
from ..header.http_headers import HTTP11, HTTPStatus
from ..header import websocket_headers

class Terminate(Exception):
    pass

class Client:

    def __init__(self, client, host, port) -> None:
        self.CLIENT = client
        self.ADDR = (host, port)
        self.HOST = host
        self.PORT = port

class _WebSocket:

    def __init__(self):
        self.CLIENTS = []
        self.TERMINATE = False
    
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

        for connected_client in self.CLIENTS:
            
            if connected_client.HOST == host and connected_client.PORT == port:
                return True

        self.CLIENTS.append(Client(client, host, port))    

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
        self.serv_func(self, client, addr)

    def client(self):

        def wrapper(func):
            self.serv_func = func

        return wrapper

    def broadcast(self, msg: str) -> None:
        for client in self.CLIENTS:
            self.send(client.CLIENT, client.ADDR, msg)

    def recv(self, client, addr) -> str:
        rec = client.recv(0xfffffff)
        logging.info(f"Recieve data from {addr[0]}:{addr[1]}")
        logging.debug(f"MSG: {rec}")
        websocket_frame = websocket_headers.WebSocket(rec).to_dict()
        opcode = websocket_frame["OpCode"]

        if opcode == websocket_headers.OpCode.CLOSE:
            self.terminate(client)
            return "A Websocket was closed"
        elif opcode == websocket_headers.OpCode.TEXT:
            return websocket_frame["Payload data"]
        else:
            raise ValueError("Invalid OpCode recieved")

    def send(self, client, addr, msg: str) -> None:
        payload = websocket_headers.WebSocket()
        payload.create(msg)
        client.send(payload.raw())
        logging.info(f"Send data to {addr[0]}:{addr[1]}")
        logging.debug(f"MSG: {msg}")

    def terminate(self, client) -> None:

        client.close()
        target = None
        self.TERMINATE = True

        for clientSocket in self.CLIENTS:

            if clientSocket.CLIENT == client:
                target = clientSocket
                break
        
        self.CLIENTS.remove(target)
        
        raise Terminate

class WebSocket(_WebSocket):

    def __init__(self, host: str, port: int, backlog: int) -> None:
        super().__init__()
        self.SOCKET = Server(host, port, backlog)

        @self.SOCKET.client()
        def _(client, addr) -> bool:

            try:

                self._register(client, addr) if not self._check_register(addr[0], addr[1], client) else self._serve(client, addr)
                return False

            except Terminate:
                return True

            except socket.timeout:
                logging.info(f"Websocket closed because timeout")
                self.terminate(client)

            except Exception as e:
                traceback.print_exc()
                logging.error(f'Meet error: {e}')
                self.terminate(client)

    def run(self):
        self.SOCKET.run()