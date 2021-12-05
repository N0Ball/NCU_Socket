# Introduction

A simple header parser (expected for a broader usage)

# HTTP

since http's header is pure readable text, the only thing to do is to parse every [`CRLF`](https://stackoverflow.com/questions/1552749/difference-between-cr-lf-lf-and-cr-line-break-types) and **ended with an empty line**.

only http 1.1 is finished

# WebSocket

**Main Frame**
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

- **FIN** : frame finished?
- **RSV1 ~ 3**: reserved 0 (or it will be too complicated)
- **opcode**: operation code
  - 0x0： A continuous frame
  - 0x1：`text payload`
  - 0x2：`binary payload`
  - 0x3-7：reserved code
  - 0x8：`close`
  - 0x9：`ping`
  - 0xA：`pong`
  - 0xB-F：reserved code.
- **mask**: payload is mask?
- **Payload Length**: payload length
- **Extended payload length**: while payload length > 125
  - 2 bytes `uint` (if payload length == 126)
  - 8 bytes `uint` (if payload length == 127)
  - 128? (NA -> Since the bit is for `mask`)
- **Masking key**: mask key
  - only appears if `mask` = 1 (true)
- **Payload Data**: payload data
  - len(payload data) = `Payload Length` or `Extended payload length`