class Header:

    def __init__(self, header) -> None:
        self.HEADER = header
        self.HEADERS = None

    def _parser(self) -> dict:
        pass

    def to_dict(self) -> dict:
        return self._parser()

    def __str__(self) -> str:

        return self.HEADER