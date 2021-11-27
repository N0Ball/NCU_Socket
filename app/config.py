import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST") or 'localhost'
PORT = os.getenv("PORT") or 8000
BACKLOG = os.getenv("BACKLOG") or 10


class BASEMODE:

    def __init__(self) -> None:
        pass

    def __dict__(self):

        return {
            "MODE": self.MODE,
            "PORT": int(self.PORT),
            "HOST": self.HOST,
            "BACKLOG": int(self.BACKLOG)
        }

    def __call__(self) -> dict:
        return self.__dict__()

class Dev(BASEMODE):

    def __init__(self) -> None:
        super().__init__()
        self.MODE = "Development"
        self.PORT = 8000
        self.HOST = 'localhost'
        self.BACKLOG = 10

class Deploy(BASEMODE):

    def __init__(self) -> None:
        super().__init__()
        self.MODE = "Deployment"
        self.PORT = os.getenv('PORT') or '0.0.0.0'
        self.HOST = os.getenv('HOST') or 8000
        self.BACKLOG = 10

class Debug(Dev):

    def __init__(self) -> None:
        super().__init__()
        self.DEBUG = "Debugging"


def getModeConfig(status: str) -> BASEMODE:

    res = {
        "DEBUG": Debug(),
        "DEV": Dev(),
        "DEPLOY": Deploy()
    }.get(status, None)

    if res == None:
        raise ValueError("No such Mode")

    return res