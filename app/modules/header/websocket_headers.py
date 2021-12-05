from bitstring import BitArray
from typing import ByteString
from .base import Header

"""
Frame format:  
​​
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
"""

class OpCode:

    TEXT = 0x1
    BINARY = 0x2
    CLOSE = 0x8
    PING = 0x9
    PONG = 0xa

class WebSocket(Header):

    def __init__(self, header: ByteString = None) -> None:
        super().__init__(header)
        self.HEADERS = {
            "FIN": 1,
            "RSV1": 1,
            "RSV2": 1,
            "RSV3": 1,
            "OpCode": 4,
            "Mask": 1,
            "PL_len": 7,
            "Extended payload length": None,
            "Mask-Key": 32,
            "Payload data": None 
        }

    def create(self, msg: str, opcode: OpCode = OpCode.TEXT, fin: bool = True):
        length = len(msg)
        msg = msg.encode('utf-8')
        payload_len = 0
        extend_len = 0

        if length > 0xffffffffffffffff:
            raise BufferError("Msg too long")
        elif length > 0xffff:
            payload_len = 127
            extend_len = length
        elif length > (0xff >> 1) - 2:
            payload_len = 126
            extend_len = length
        else:
            payload_len = length
        
        payload = bytes([(fin << 7) + opcode])
        payload += payload_len.to_bytes(1, byteorder='big')
        if extend_len == 0:
            payload += msg
        elif payload_len == 126:
            payload += extend_len.to_bytes(2, byteorder='big') + msg
        elif payload_len == 127:
            payload += extend_len.to_bytes(8, byteorder='big') + msg
        else:
            raise SystemError("payload_len is not correctlly set")

        self.HEADER = payload

    def _parser(self) -> None:

        TEMP_HEADER = {}
        header_index = 0
        
        for header in self.HEADERS:

            header_len = self.HEADERS[header]

            if header == "Extended payload length":

                if TEMP_HEADER["PL_len"] == 126:
                    header_len = 16
                elif TEMP_HEADER["PL_len"] == 127:
                    header_len = 64
                else:
                    header_len = 0

            if header == "Mask-Key":

                header_len = self.HEADERS[header] if TEMP_HEADER["Mask"] == 1 else 0

            if header == "Payload data":

                header_len = TEMP_HEADER["PL_len"] if TEMP_HEADER["Extended payload length"] == None else TEMP_HEADER["Extended payload length"]

                target = self.HEADER[header_index // 8 : header_index // 8 + header_len]
                if TEMP_HEADER["Mask"] == 1:
                    TEMP_HEADER["Mask-Key"] = list(map(lambda i: TEMP_HEADER["Mask-Key"] >> ((3 - i)*8) & 0xff, range(4)))
                    target = list(target)
                    for i in range(len(target)):
                        target[i] = chr(target[i] ^ TEMP_HEADER["Mask-Key"][i % 4])
                    target = ''.join(target).encode('utf-8')

                target = target.decode('utf-8')

            else:
                target = self.get_data(self.HEADER, header_index, header_len)
                header_index += header_len
            
            TEMP_HEADER.update({header: target})

        self.HEADER = TEMP_HEADER
        return TEMP_HEADER

    def get_data(self, header, index, len):

        res = BitArray(bytes=header, length=len, offset=index)

        if not len == 0:
            return int(res.bin, 2)
        else:
            return None

    def raw(self) -> ByteString:
        return self.HEADER
