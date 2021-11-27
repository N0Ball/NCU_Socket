import unittest

from ..server import create_accept

class WebSocketTestCase(unittest.TestCase):
    
    def test_create_accpet(self):
        accpet = create_accept('dGhlIHNhbXBsZSBub25jZQ==')
        self.assertEqual(accpet, 's3pPLMBiTxaQ9kYGzzhZRbK+xOo=')


if __name__ == '__main__':

    unittest.main()