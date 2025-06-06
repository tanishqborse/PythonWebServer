import unittest
from basic_parser import parse_req

class TestParseReq(unittest.TestCase):
    def test_get_root_returns_200(self):
        request = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
        response = parse_req(request)
        self.assertIn("HTTP/1.1 200 OK", response)

    def test_invalid_method_returns_400(self):
        request = "FETCH / HTTP/1.1\r\nHost: localhost\r\n\r\n"
        response = parse_req(request)
        self.assertIn("HTTP/1.1 400 Bad Request", response)

if __name__ == "__main__":
    unittest.main()
