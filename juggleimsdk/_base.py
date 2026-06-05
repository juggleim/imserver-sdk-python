"""Core HTTP client."""

from __future__ import annotations

import json
from typing import Any, Optional, Tuple, Type, TypeVar

from juggleimsdk.util import (
    ApiCode,
    build_headers,
    from_dict,
    generate_uuid_short11,
    http_do_bytes,
    to_json_dict,
)

T = TypeVar("T")

DEFAULT_API_URL = ""


class HttpClient:
    """Base HTTP client for JuggleIM Server API."""

    def __init__(self, appkey: str, secret: str, api_url: str = DEFAULT_API_URL) -> None:
        self.appkey = appkey
        self.secret = secret
        self.api_url = api_url

    def http_call(
        self,
        method: str,
        url_path: str,
        req: Any = None,
        resp_cls: Optional[Type[T]] = None,
        *,
        resp_is_list: bool = False,
    ) -> Tuple[Optional[T], ApiCode, str, Optional[Exception]]:
        url = self.api_url + url_path
        trace_id = generate_uuid_short11()
        headers = build_headers(self.appkey, self.secret)
        body = ""

        if method.upper() == "POST":
            body = json.dumps(to_json_dict(req) if req is not None else {})
        elif method.upper() != "GET":
            return None, ApiCode.NOT_SUPPORT_METHOD, trace_id, Exception(
                f"not support method:{method}"
            )

        try:
            resp_bytes = http_do_bytes(method.upper(), url, headers, body)
        except Exception as exc:
            return None, ApiCode.HTTP_TIMEOUT, trace_id, exc

        try:
            payload = json.loads(resp_bytes.decode("utf-8"))
        except json.JSONDecodeError as exc:
            return None, ApiCode.DECODE_FAIL, trace_id, exc

        raw_code = payload.get("code", -1)
        try:
            code = ApiCode(raw_code)
        except ValueError:
            code = raw_code  # type: ignore[assignment]
        msg = payload.get("msg", "")
        data = payload.get("data")

        if code != ApiCode.SUCCESS:
            return None, code, trace_id, Exception(msg)

        if resp_cls is None:
            return None, ApiCode.SUCCESS, trace_id, None

        if data is None:
            return None, ApiCode.DECODE_FAIL, trace_id, Exception("decode fail")

        if resp_is_list:
            item_type = resp_cls.__args__[0] if hasattr(resp_cls, "__args__") else resp_cls
            parsed = [from_dict(item_type, item) for item in data]
            return parsed, ApiCode.SUCCESS, trace_id, None  # type: ignore[return-value]

        return from_dict(resp_cls, data), ApiCode.SUCCESS, trace_id, None

    def _post(
        self, url_path: str, req: Any = None
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        _, code, trace_id, err = self.http_call("POST", url_path, req)
        return code, trace_id, err

    def _get(
        self, url_path: str, resp_cls: Type[T]
    ) -> Tuple[Optional[T], ApiCode, str, Optional[Exception]]:
        return self.http_call("GET", url_path, resp_cls=resp_cls)
