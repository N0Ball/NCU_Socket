import logging
import threading
from socket import socket, AF_INET, SOCK_STREAM, timeout

class Server:

    def __init__(self, host: str, port: int, backlog: int) -> None:
        self.HOST = host 
        self.PORT = port 
        self.BACKLOG = backlog
        self.TIMEOUT = 0.2
        self.client_response = None

    def run(self) -> None:

        self.SERVER = socket(AF_INET, SOCK_STREAM)
        self.SERVER.bind((self.HOST, self.PORT))
        self.SERVER.listen(self.BACKLOG)
        self.SERVER.settimeout(self.TIMEOUT)

        logging.info(f"Socket is now listening at {self.HOST}:{self.PORT}")

        while True:

            try:
                conn, addr = self.SERVER.accept()
                conn.settimeout(60)
                logging.debug(f"Connected to {addr[0]}:{addr[1]}")
                threading.Thread(target = self.client_conn, args = (conn, addr)).start()
            except timeout:
                pass
            except KeyboardInterrupt:
                break

         
        self.SERVER.close()
        logging.info(f"Socket closed Successfully")

        import os
        os._exit(0)

    def client(self):
        
        def wrapper(func):
            self.client_response = func
            return func

        return wrapper

    def client_conn(self, client, addr) -> bool:

        logging.info(f"Connected to client at {addr[0]}:{addr[1]}")

        while True:

            try:
                if self.client_response(client, addr):
                    client.close()
                    break
            except:
                client.close()
                return False

        logging.info(f"Disconnected to client {addr[0]}:{addr[1]}")