from abc import ABC, abstractmethod
from .base import Header

class HTTPStatus:

    def __init__(self, code: int, msg: str = None) -> None:
        self.code = code
        self.msg = msg or ''

class HTTP(Header, ABC):

    def __init__(self, header) -> None:
        super().__init__(header)

    def _parser(self) -> str:

        parsed_headers = self.HEADER.split('\r\n')
        version_location = parsed_headers[0].find('HTTP/')

        VERSION_SIZE = 8

        if version_location == -1:
            raise ValueError("No HTTP version was find in the header")

        version = parsed_headers[0][version_location:version_location+VERSION_SIZE]
        print(version)

        self._checkVersion(version)

        self.HEADERS = {}
        for header in parsed_headers:
            
            key, *value = header.split(': ')

            if len(value) == 1:
                self.HEADERS.update({key: value[0]})
            else:
                self.HEADERS.update({key: value})

        return self.HEADERS

    @abstractmethod
    def _checkVersion(self, version: str) -> None:
        pass

    def setResponseHeader(self, status: HTTPStatus, **headers):
        self.HEADER = "HTTP/1.1 " + str(status.code) + ' ' + status.msg + '\r\n'

        for key in headers:
            self.HEADER += key + ": " + headers.get(key) + '\r\n'

        self.HEADER += '\r\n'

class HTTP11(HTTP):

    def __init__(self, header: str = None) -> None:
        super().__init__(header)
        self.TYPE = "HTTP 1.1"

    def _checkVersion(self, version: str) -> None:
        if not version.upper() == 'HTTP/1.1':
            raise TypeError("Only HTTP version 1.1 are permitted")