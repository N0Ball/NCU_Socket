import unittest

from app.config import getModeConfig

class ConfigTestCase(unittest.TestCase):

    def _test_config(self, mode, expt_port, expt_host):
        mode = getModeConfig(mode)()
        self.assertEqual(mode["PORT"], expt_port)
        self.assertEqual(mode["HOST"], expt_host)

    def _test_config_failed(self, mode, expt_msg):
        with self.assertRaises(ValueError) as e:
            mode = getModeConfig(mode)
        
        self.assertEqual(str(e.exception), expt_msg)

    def test_dev(self):
        self._test_config("DEV", 8000, 'localhost')
    def test_debug(self):
        self._test_config("DEPLOY", 5000, '0.0.0.0')
    def test_no_such_mode(self):
        self._test_config_failed("OUO", "No such Mode")

if __name__ == '__main__':
    unittest.main()