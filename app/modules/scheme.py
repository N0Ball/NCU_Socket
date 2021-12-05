from typing import Optional
from pydantic import BaseModel

class ClientOperation(object):

    PING=0x1
    PONG=0x2
    MSG =0x3
    MOVE=0x4

class Com(BaseModel):
    
    OP: int
    DATA: Optional[str]