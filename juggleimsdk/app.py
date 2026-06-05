"""App / Connect API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from juggleimsdk._base import HttpClient
from juggleimsdk.util import ApiCode


@dataclass
class RestrictedFields:
    max_user_count: int = 0


@dataclass
class AppInfo:
    app_type: int = 0
    app_name: str = ""
    created_time: int = 0
    update_time: int = 0
    app_key: str = ""
    app_secret: str = ""
    app_status: int = 0
    max_user_count: int = 0
    cur_user_count: int = 0
    restricted_fields: Optional[RestrictedFields] = None
    config_fields: Optional[Dict[str, str]] = None
    expired_time: int = 0
    license_conf: str = ""


@dataclass
class ActiveAppReq:
    license: str = ""


@dataclass
class ConnectSignKeysReq:
    sign_keys: List[str] = field(default_factory=list)


@dataclass
class ConnectSignKeysResp:
    sign_keys: Optional[List[str]] = None


class AppApiMixin:
    def add_connect_sign_keys(
        self: HttpClient, sign_keys: List[str]
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post(
            "/apigateway/connectsignkeys/add", ConnectSignKeysReq(sign_keys=sign_keys)
        )

    def qry_connect_sign_keys(
        self: HttpClient,
    ) -> Tuple[Optional[ConnectSignKeysResp], ApiCode, str, Optional[Exception]]:
        return self._get("/apigateway/connectsignkeys/query", ConnectSignKeysResp)

    def add_app_connect_sign_keys(
        self: HttpClient, sign_keys: List[str]
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post(
            "/apigateway/apps/connectsignkeys/add", ConnectSignKeysReq(sign_keys=sign_keys)
        )

    def qry_app_connect_sign_keys(
        self: HttpClient,
    ) -> Tuple[Optional[ConnectSignKeysResp], ApiCode, str, Optional[Exception]]:
        return self._get("/apigateway/apps/connectsignkeys/query", ConnectSignKeysResp)
