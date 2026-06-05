"""Global mute API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from juggleimsdk._base import HttpClient
from juggleimsdk.util import ApiCode


@dataclass
class UserIds:
    user_ids: List[str] = field(default_factory=list)


@dataclass
class MuteUser:
    user_id: str = ""
    created_time: int = 0


@dataclass
class QryMuteUsersResp:
    items: Optional[List[MuteUser]] = None
    offset: str = ""


class MuteApiMixin:
    def add_private_global_mute_members(
        self: HttpClient, user_ids: List[str]
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post(
            "/apigateway/private/globalmutemembers/add", UserIds(user_ids=user_ids)
        )

    def del_private_global_mute_members(
        self: HttpClient, user_ids: List[str]
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post(
            "/apigateway/private/globalmutemembers/del", UserIds(user_ids=user_ids)
        )

    def qry_private_global_mute_members(
        self: HttpClient, limit: int, offset: str
    ) -> Tuple[Optional[QryMuteUsersResp], ApiCode, str, Optional[Exception]]:
        return self._get(
            f"/apigateway/private/globalmutemembers/query?limit={limit}&offset={offset}",
            QryMuteUsersResp,
        )

    def add_group_global_mute_members(
        self: HttpClient, user_ids: List[str]
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/group/globalmutemembers/add", UserIds(user_ids=user_ids))

    def del_group_global_mute_members(
        self: HttpClient, user_ids: List[str]
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/group/globalmutemembers/del", UserIds(user_ids=user_ids))

    def qry_group_global_mute_members(
        self: HttpClient, limit: int, offset: str
    ) -> Tuple[Optional[QryMuteUsersResp], ApiCode, str, Optional[Exception]]:
        return self._get(
            f"/apigateway/group/globalmutemembers/query?limit={limit}&offset={offset}",
            QryMuteUsersResp,
        )
