# Introduction 

A simple websocket server derived from [socket server](../socket/README.md)

> The most annoying thing of all 

# Technologies

The server has to connect to a web browser, which means that it requires a minimal of APIs for it to work normally.

A basic websocket looks like this <br>
![](https://upload.wikimedia.org/wikipedia/commons/1/10/Websocket_connection.png) <br>
which requires three basic component

1. HTTP Handshake
2. Keep Connections & Communicate
3. Close Channel

## HTTP Handshake

That's why not only a websocket server, a normal HTTP web server is also needed for a websocket connection.

You should go through [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers) if you need a throughout knowledge

A simple websocket request looks like this.
```
GET / HTTP/1.1
Host: example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

The server should reply with
```
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

**Where** `Sec-WebSocket-Accept` is concatenate the client's `Sec-WebSocket-Key` and the string `258EAFA5-E914-47DA-95CA-C5AB0DC85B11`, take the `SHA-1 hash` and return the `base64`

which can be simply written as a python code 
> Which is the exactly why I chose python instead of C for this project
```python
import hashlib
import base64
def get_accept(self, key: str) -> str:
    method = hashlib.sha1()
    method.update((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode('utf-8'))
    return base64.b64encode(method.digest()).decode('utf-8')
```

After replying to the web browser, both the web browser and you knows that both of you are going to communicate with websocket.

## Keep Connections & Communicate

Since websocket doesn't need other packates while communication, the connections is actually not so reliable, that is, a [heartbeat](https://stackoverflow.com/questions/46111656/must-websockets-have-heartbeats) is needed to test the connections between the host and the user.

The frame format of the websocket
```
0                   1                   2                   3
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-------+-+-------------+-------------------------------+
|F|R|R|R| opcode|M| Payload len |    Extended payload length    |
|I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
|N|V|V|V|       |S|             |   (if payload len==126/127)   |
| |1|2|3|       |K|             |                               |
+-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
|     Extended payload length continued, if payload len == 127  |
+ - - - - - - - - - - - - - - - +-------------------------------+
|                               |Masking-key, if MASK set to 1  |
+-------------------------------+-------------------------------+
| Masking-key (continued)       |          Payload Data         |
+-------------------------------- - - - - - - - - - - - - - - - +
:                     Payload Data continued ...                :
+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
|                     Payload Data continued ...                |
+---------------------------------------------------------------+
```

The most interesting part is the extended payload length and the mask.
But this will be discussed in the [Header](../header/README.md) part.

### Heartbeat

Every a period of seconds, the server should `ping` the client, making sure that the client `pong` back, which means that the connection is still normal.

signal alarm is implemented here to step out the while loop. Since, multithreading is used in socket server, it's not a great idea to implement an `asyncio` in every threads.
```python
import signal

HEARTBEAT_PASSTIME = 10 # seconds

def heartbeat_handler():

    # ...
    # heat beat code
    # ...

    signal.alarm(HEARTMEAT_PASSTIME)

signal.signal(signal.SIGALRM, heartbeat_handler)
signal.alarm(HEARTBEAT_PASSTIME)
```

where heartbeat only sends a random string to `client` and `echo` back to the server.

## Close Websocket

It's included in the `websocket frame`.
A `0` length `payload data` sended with an `opcode` set to `0x8` is all it needs.

# Usage

A simple echo server that `broadcast` the upper of the client's message.
```python

from websocket.server import Websocket

HOST='localhost'
PORT=8000
BACKLOG=10

SERVER = Websocket(HOST, PORT, BACKLOG)

@SERVER.client()
def _(self, client, addr):

    msg = self.recv(client, addr)
    print(f"receved message from {addr[0]}:{addr[1]}")
    self.broadcast(client, addr, msg.topper())

if __name__ == '__main__':
    SERVER.run()
```

**Since** Websocket keeps alive **every connections**, so it is very easy to broadcast to all users online.