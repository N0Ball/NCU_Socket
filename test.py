from app.modules.header.http_headers import HTTP11, HTTPStatus

a = HTTP11()
a.setResponseHeader(
    HTTPStatus(101, 'Switching Protocols'), 
    Upgrade="websocket",
    Connection="upgrade"
)

print(str(a))