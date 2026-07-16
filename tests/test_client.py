import json
import unittest
from unittest.mock import patch

from juggleimsdk import ApiCode, User, new_juggle_im_sdk


class ClientTest(unittest.TestCase):
    def setUp(self):
        self.sdk = new_juggle_im_sdk("app-key", "app-secret", "http://localhost:9001")

    @patch("juggleimsdk._base.http_do_bytes")
    def test_register_maps_success_response(self, http_do_bytes):
        http_do_bytes.return_value = json.dumps(
            {
                "code": 0,
                "data": {"user_id": "alice", "token": "token-1"},
            }
        ).encode("utf-8")

        user, code, trace_id, error = self.sdk.register(
            User(user_id="alice", nickname="Alice")
        )

        self.assertEqual(ApiCode.SUCCESS, code)
        self.assertIsNone(error)
        self.assertEqual("alice", user.user_id)
        self.assertEqual("token-1", user.token)
        self.assertEqual(11, len(trace_id))

        method, url, headers, body = http_do_bytes.call_args.args
        self.assertEqual("POST", method)
        self.assertEqual("http://localhost:9001/apigateway/users/register", url)
        self.assertEqual("app-key", headers["appkey"])
        self.assertEqual(
            {"user_id": "alice", "nickname": "Alice", "user_portrait": "", "is_admin": False},
            json.loads(body),
        )

    @patch("juggleimsdk._base.http_do_bytes")
    def test_api_error_preserves_server_code_and_message(self, http_do_bytes):
        http_do_bytes.return_value = b'{"code":1001,"msg":"permission denied"}'

        user, code, trace_id, error = self.sdk.register(User(user_id="alice"))

        self.assertIsNone(user)
        self.assertEqual(1001, code)
        self.assertEqual(11, len(trace_id))
        self.assertEqual("permission denied", str(error))

    @patch("juggleimsdk._base.http_do_bytes", return_value=b"not-json")
    def test_invalid_json_returns_decode_failure(self, _http_do_bytes):
        user, code, trace_id, error = self.sdk.register(User(user_id="alice"))

        self.assertIsNone(user)
        self.assertEqual(ApiCode.DECODE_FAIL, code)
        self.assertEqual(11, len(trace_id))
        self.assertIsNotNone(error)

    def test_unsupported_method_returns_local_error(self):
        data, code, trace_id, error = self.sdk.http_call("PUT", "/resource")

        self.assertIsNone(data)
        self.assertEqual(ApiCode.NOT_SUPPORT_METHOD, code)
        self.assertEqual(11, len(trace_id))
        self.assertEqual("not support method:PUT", str(error))


if __name__ == "__main__":
    unittest.main()
