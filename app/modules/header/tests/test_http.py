import unittest

from ..http_headers import HTTP11, HTTPStatus

NORMAL_HTTP11_HEADER = """\
GET /a/b HTTP/1.1\r
Host: example.com\r
User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)\r
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r
Accept-Language: en-us,en;q=0.5\r
Accept-Encoding: gzip,deflate\r
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7\r
Keep-Alive: 300\r
Connection: keep-alive\r
Test-Data: test-data_123\r
Cookie: PHPSESSID=r2t5uvjq435r4q7ib3vtdjq120\r
Pragma: no-cache\r
Cache-Control: no-cache\r
\r
"""

FAILED_HTTP11_HEADER = """\
GET /a/b HTTP/1.0\r
Host: example.com\r
User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)\r
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r
Accept-Language: en-us,en;q=0.5\r
Accept-Encoding: gzip,deflate\r
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7\r
Keep-Alive: 300\r
Connection: keep-alive\r
Test-Data: test-data_123\r
Cookie: PHPSESSID=r2t5uvjq435r4q7ib3vtdjq120\r
Pragma: no-cache\r
Cache-Control: no-cache\r
\r
"""

RESULT_HTTP11_HEADER = b"""\
HTTP/1.1 200 OK\r
Age: 521648\r
Keep-Alive: 300\r
\r
"""

class HTTPHeaderTestCase(unittest.TestCase):

    def _test_http11_header(self, raw_header, expt):
        header = HTTP11(raw_header).to_dict()
        self.assertEqual(header['Test-Data'], expt)

    def _test_http11_create_header(self, code, msg, expt, **headers):
        header = HTTP11()
        header.setResponseHeader(
            HTTPStatus(code, msg),
            **headers
        )

        self.assertEqual(expt, header.raw())

    def _test_http11_version_failed(self, raw_header, expt):
        with self.assertRaises(TypeError) as e:
            _ = HTTP11(raw_header).to_dict()
        self.assertEqual(str(e.exception), expt)

    def test_normal_http1(self):
        self._test_http11_header(NORMAL_HTTP11_HEADER, "test-data_123")
    def test_http11_version_failed(self):
        self._test_http11_version_failed(FAILED_HTTP11_HEADER, "Only HTTP version 1.1 are permitted")
    def test_create_http1(self):
        self._test_http11_create_header(200, 'OK', RESULT_HTTP11_HEADER, **{
            "Age": 521648,
            "Keep-Alive": 300,
        })

if __name__ == '__main__':
    unittest.main()