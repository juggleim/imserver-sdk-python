import unittest
from unittest.mock import patch

from juggleimsdk.util import build_headers, sha1


class UtilTest(unittest.TestCase):
    @patch("juggleimsdk.util.time.time", return_value=1234.567)
    @patch("juggleimsdk.util.random.randint", return_value=42)
    def test_build_headers_signs_secret_nonce_and_timestamp(self, _randint, _time):
        headers = build_headers("app-key", "app-secret")

        self.assertEqual("application/json", headers["Content-Type"])
        self.assertEqual("app-key", headers["appkey"])
        self.assertEqual("42", headers["nonce"])
        self.assertEqual("1234567", headers["timestamp"])
        self.assertEqual(sha1("app-secret421234567"), headers["signature"])


if __name__ == "__main__":
    unittest.main()
