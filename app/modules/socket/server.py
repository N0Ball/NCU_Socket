import logging
import threading
from socket import socket, AF_INET, SOCK_STREAM, timeout

class Server:

    def __init__(self, host: str, port: int, backlog: int) -> None:
        self.HOST = host 
        self.PORT = port 
        self.BACKLOG = backlog
        self.TIMEOUT = 0.2

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
                logging.info(f"Connected to {addr[0]}:{addr[1]}")
                threading.Thread(target = self.client_conn, args = (conn, addr)).start()
            except timeout:
                pass
            except KeyboardInterrupt:
                break

         
        self.SERVER.close()
        logging.info(f"Socket closed Successfully")

    def client_conn(self, client, addr) -> bool:

        logging.info(f"Connecting to client at {addr[0]}:{addr[1]}")

        while True:

            try:
                msg: str = str(client.recv(1024), encoding='utf-8')
                logging.info(f"Recved message from {addr[0]}:{addr[1]} > {msg}")

                if msg == "exit":
                    print("OUO")
                    logging.info(f'{addr[0]}:{addr[1]} disconnected')
                    client.close()
                    return False
                elif msg:
                    logging.info(f"Sending message to {addr[0]}:{addr[1]} > {msg.upper()}")
                    client.send("""
HTTP/1.1 101 Switching Protocols\r
Upgrade: websocket\r
Connection: Upgrade\r
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=\r
\r
""".encode('utf-8'))
                else:
                    print("AAA")
                    raise Exception("OUO")

            except:
                client.close()
                return False
