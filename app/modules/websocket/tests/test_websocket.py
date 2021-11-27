import unittest

from ..server import _WebSocket

class WebSocketTestCase(unittest.TestCase):
    
    def test_create_accpet(self):
        webSocket = _WebSocket()
        accpet = webSocket._get_accept('dGhlIHNhbXBsZSBub25jZQ==')
        self.assertEqual(accpet, 's3pPLMBiTxaQ9kYGzzhZRbK+xOo=')


if __name__ == '__main__':

    unittest.main()