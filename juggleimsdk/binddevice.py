"""Bind device API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

from juggleimsdk._base import HttpClient
from juggleimsdk.util import ApiCode


@dataclass
class BindDevice:
    user_id: str = ""
    device_id: str = ""
    platform: str = ""
    device_company: str = ""
    device_model: str = ""
    created_time: int = 0


@dataclass
class BindDevicesResp:
    items: Optional[List[BindDevice]] = None


class BindDeviceApiMixin:
    def add_bind_device(
        self: HttpClient, device: BindDevice
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/binddevices/add", device)

    def del_bind_device(
        self: HttpClient, device: BindDevice
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/binddevices/del", device)

    def qry_bind_devices(
        self: HttpClient, user_id: str
    ) -> Tuple[Optional[BindDevicesResp], ApiCode, str, Optional[Exception]]:
        return self._get(f"/apigateway/binddevices/query?user_id={user_id}", BindDevicesResp)
