"""User API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from juggleimsdk._base import HttpClient
from juggleimsdk.util import ApiCode


class UserSettingKey:
    LANGUAGE = "language"
    UNDISTURB = "undisturb"


@dataclass
class PermitConver:
    target_id: str = ""
    target_id_alias: str = ""
    channel_type: int = 0
    max_his_msg_count: int = 0


@dataclass
class User:
    user_id: str = ""
    nickname: str = ""
    user_portrait: str = ""
    ext_fields: Optional[Dict[str, str]] = None
    settings: Optional[Dict[str, str]] = None
    is_admin: bool = False
    permit_conver: Optional[PermitConver] = None
    permit_convers: Optional[List[PermitConver]] = None


@dataclass
class UserRegResp:
    user_id: str = ""
    token: str = ""


@dataclass
class UserOnlineStatusReq:
    user_ids: List[str] = field(default_factory=list)


@dataclass
class UserOnlineStatusItem:
    user_id: str = ""
    is_online: bool = False


@dataclass
class UserOnlineStatusResp:
    items: Optional[List[UserOnlineStatusItem]] = None


@dataclass
class BanUser:
    user_id: str = ""
    created_time: int = 0
    end_time: int = 0
    end_time_offset: int = 0
    scope_key: str = ""
    scope_value: str = ""
    ext: str = ""


@dataclass
class BanUsers:
    items: Optional[List[BanUser]] = None
    offset: str = ""


@dataclass
class KickUserReq:
    user_id: str = ""
    platforms: Optional[List[str]] = None
    device_ids: Optional[List[str]] = None
    ext: str = ""


@dataclass
class BlockUsersReq:
    user_id: str = ""
    block_user_ids: Optional[List[str]] = None


@dataclass
class BlockUser:
    block_user_id: str = ""
    createed_time: int = 0


@dataclass
class QryBlockUsersResp:
    user_id: str = ""
    items: Optional[List[BlockUser]] = None
    offset: str = ""


class UserApiMixin:
    def register(
        self: HttpClient, user: User
    ) -> Tuple[Optional[UserRegResp], ApiCode, str, Optional[Exception]]:
        return self.http_call("POST", "/apigateway/users/register", user, UserRegResp)

    def update_user(self: HttpClient, user: User) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/users/update", user)

    def qry_user_info(
        self: HttpClient, user_id: str
    ) -> Tuple[Optional[User], ApiCode, str, Optional[Exception]]:
        return self._get(f"/apigateway/users/info?user_id={user_id}", User)

    def set_user_settings(
        self: HttpClient, user: User
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/users/settings/set", user)

    def get_user_settings(
        self: HttpClient, user_id: str
    ) -> Tuple[Optional[User], ApiCode, str, Optional[Exception]]:
        return self._get(f"/apigateway/users/settings/get?user_id={user_id}", User)

    def qry_user_online_status(
        self: HttpClient, user_ids: List[str]
    ) -> Tuple[Optional[UserOnlineStatusResp], ApiCode, str, Optional[Exception]]:
        return self.http_call(
            "POST",
            "/apigateway/users/onlinestatus/query",
            UserOnlineStatusReq(user_ids=user_ids),
            UserOnlineStatusResp,
        )

    def ban_users(
        self: HttpClient, ban_users: BanUsers
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/users/banusers/ban", ban_users)

    def un_ban_users(
        self: HttpClient, ban_users: BanUsers
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/users/banusers/unban", ban_users)

    def qry_ban_users(
        self: HttpClient, limit: int, offset: str
    ) -> Tuple[Optional[BanUsers], ApiCode, str, Optional[Exception]]:
        return self._get(
            f"/apigateway/users/banusers/query?limit={limit}&offset={offset}", BanUsers
        )

    def qry_ban_users_by_user_ids(
        self: HttpClient, user_ids: List[str]
    ) -> Tuple[Optional[BanUsers], ApiCode, str, Optional[Exception]]:
        if not user_ids:
            return BanUsers(), ApiCode.SUCCESS, "", None
        params = "&".join(f"user_id={uid}" for uid in user_ids)
        return self._get(f"/apigateway/users/banusers/query?{params}", BanUsers)

    def kick_users(
        self: HttpClient, req: KickUserReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/users/kick", req)

    def block_user(
        self: HttpClient, req: BlockUsersReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/users/blockusers/block", req)

    def un_block_user(
        self: HttpClient, req: BlockUsersReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/users/blockusers/unblock", req)

    def qry_block_users(
        self: HttpClient, user_id: str, limit: int, offset: str
    ) -> Tuple[Optional[QryBlockUsersResp], ApiCode, str, Optional[Exception]]:
        return self._get(
            f"/apigateway/users/blockusers/query?user_id={user_id}&limit={limit}&offset={offset}",
            QryBlockUsersResp,
        )
