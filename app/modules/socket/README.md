# Introduction

A Simple Socket Server 

# Usage


A Simple echo server that returns the uppercase of the sent message
```python
from socket.server import Socket

HOST='localhost'
PORT=8000
BACKLOG=10

SERVER = new Socket(HOST, PORT, BACKLOG)

@SERVER.client()
def _(self, client, addr){
    msg = client.recv(1024).decode('utf-8').upper()
    print(f"Get msg from {addr[0]}:{addr[1]}")
    client.send(msg.encode('utf-8'))
}

if __name__ == '__main__':
    SERVER.run()

```

# Cool Tech

Using python decorator, you can easily modify the server action without modifing any core code.

```python
def client(self):
    
    def wrapper(func):
        self.client_response = func
        return func

    return wrapper
```

**Therefore** the flow becomes: <br>
1. construct Socket class
2. modify Socket's client_response
3. call Socket's client_response