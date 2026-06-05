"""HTTP utilities and helpers."""

from __future__ import annotations

import hashlib
import json
import random
import struct
import time
import uuid
from dataclasses import fields, is_dataclass
from enum import IntEnum
from typing import Any, Dict, Optional, Type, TypeVar, Union
from urllib import error, request

T = TypeVar("T")

DEFAULT_API_URL = ""

DIGITS64 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_"


class ApiCode(IntEnum):
    SUCCESS = 0
    HTTP_TIMEOUT = 1
    DECODE_FAIL = 2
    NOT_SUPPORT_METHOD = 3


def sha1(value: str) -> str:
    return hashlib.sha1(value.encode("utf-8")).hexdigest()


def generate_uuid_short11() -> str:
    return shortcut(uuid2_short_string(uuid.uuid4()))


def shortcut(value: str) -> str:
    if len(value) > 16:
        return value[5:16]
    return ""


def uuid2_short_string(uid: uuid.UUID) -> str:
    uid_bytes = uid.bytes
    most_bits = uid_bytes[:8]
    least_bits = uid_bytes[8:]
    return to_id_string(struct.unpack(">Q", most_bits)[0]) + to_id_string(
        struct.unpack(">Q", least_bits)[0]
    )


def to_id_string(value: int) -> str:
    buf = bytearray(11)
    length = 11
    least = 63
    while True:
        length -= 1
        buf[length] = ord(DIGITS64[value & least])
        value >>= 6
        if value == 0:
            break
    return buf.decode("ascii")


def to_json_dict(obj: Any) -> Any:
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, list):
        return [to_json_dict(item) for item in obj]
    if isinstance(obj, dict):
        return {key: to_json_dict(val) for key, val in obj.items()}
    if is_dataclass(obj):
        result: Dict[str, Any] = {}
        for field in fields(obj):
            val = getattr(obj, field.name)
            if val is None:
                continue
            result[field.name] = to_json_dict(val)
        return result
    if hasattr(obj, "value"):
        return obj.value
    return obj


def from_dict(cls: Type[T], data: Any) -> T:
    if data is None:
        return None  # type: ignore[return-value]
    if not is_dataclass(cls):
        return data  # type: ignore[return-value]

    kwargs: Dict[str, Any] = {}
    field_types = {field.name: field.type for field in fields(cls)}
    for field in fields(cls):
        if field.name not in data:
            continue
        value = data[field.name]
        field_type = field_types[field.name]
        kwargs[field.name] = _convert_value(field_type, value)
    return cls(**kwargs)


def _convert_value(field_type: Any, value: Any) -> Any:
    if value is None:
        return None

    origin = getattr(field_type, "__origin__", None)
    if origin is Union:
        args = [arg for arg in field_type.__args__ if arg is not type(None)]
        if args:
            field_type = args[0]
            origin = getattr(field_type, "__origin__", None)

    if origin is list:
        item_type = field_type.__args__[0]
        if is_dataclass(item_type):
            return [from_dict(item_type, item) for item in value]
        return value

    if is_dataclass(field_type):
        return from_dict(field_type, value)

    return value


def http_do_bytes(
    method: str,
    url: str,
    headers: Dict[str, str],
    body: str = "",
    timeout: float = 30.0,
) -> bytes:
    data = body.encode("utf-8") if body else None
    req = request.Request(url, data=data, method=method)
    for key, val in headers.items():
        req.add_header(key, val)
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except error.URLError as exc:
        raise exc


def to_json(obj: Any) -> str:
    return json.dumps(to_json_dict(obj), ensure_ascii=False)


def build_headers(appkey: str, secret: str) -> Dict[str, str]:
    nonce = str(random.randint(0, 9999))
    timestamp = str(int(time.time() * 1000))
    signature = sha1(f"{secret}{nonce}{timestamp}")
    return {
        "Content-Type": "application/json",
        "appkey": appkey,
        "nonce": nonce,
        "timestamp": timestamp,
        "signature": signature,
    }
