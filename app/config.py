import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST") or '0.0.0.0'
PORT = int(os.getenv("PORT")) or 8000
BACKLOG = os.getenv("BACKLOG") or 10


class BASEMODE:

    def __init__(self) -> None:
        pass

class Dev(BASEMODE):

    def __init__(self) -> None:
        super().__init__()
        self.MODE = "DEV"
        self.PORT = 8000
        self.HOST = 'localhost'
        self.BACKLOG = 10

class Deploy(BASEMODE):

    def __init__(self) -> None:
        super().__init__()
        self.MODE = "DEPLOY"
        self.PORT = PORT
        self.HOST = HOST
        self.BACKLOG = 10

class Debug(Dev):

    def __init__(self) -> None:
        super().__init__()
        self.MODE = "DEBUG"


def getModeConfig(status: str) -> BASEMODE:

    res = {
        "DEBUG": Debug(),
        "DEV": Dev(),
        "DEPLOY": Deploy()
    }.get(status, None)

    if res == None:
        raise ValueError("No such Mode")
        # res = Debug()

    return res