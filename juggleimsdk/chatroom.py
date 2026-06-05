"""Chatroom API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

from juggleimsdk._base import HttpClient
from juggleimsdk.util import ApiCode


@dataclass
class ChatroomMember:
    member_id: str = ""
    member_name: str = ""
    added_time: int = 0
    end_time: int = 0


@dataclass
class ChatroomAtt:
    key: str = ""
    value: str = ""
    att_time: int = 0
    user_id: str = ""
    is_force: Optional[bool] = None


@dataclass
class ChatroomInfo:
    chat_id: str = ""
    chat_name: str = ""
    members: Optional[List[ChatroomMember]] = None
    atts: Optional[List[ChatroomAtt]] = None
    member_count: int = 0
    is_mute: int = 0


@dataclass
class ChrmBanUserReq:
    chat_id: str = ""
    member_ids: Optional[List[str]] = None
    end_time: int = 0
    end_time_offset: int = 0


@dataclass
class ChrmBanUsers:
    chat_id: str = ""
    members: Optional[List[ChatroomMember]] = None
    offset: str = ""


@dataclass
class ChrmMemberIds:
    chat_id: str = ""
    member_ids: Optional[List[str]] = None


@dataclass
class ChrmMemberExistItem:
    member_id: str = ""
    exist: bool = False


@dataclass
class ChrmMembersExistResp:
    items: Optional[List[ChrmMemberExistItem]] = None


@dataclass
class ChatroomAtts:
    from_id: str = ""
    chat_id: str = ""
    atts: Optional[List[ChatroomAtt]] = None


@dataclass
class ChatroomAttResp:
    key: str = ""
    code: int = 0
    att_time: int = 0


@dataclass
class ChatroomAttsResp:
    atts: Optional[List[ChatroomAttResp]] = None


@dataclass
class ChatroomAttsReq:
    chat_id: str = ""
    att_keys: Optional[List[str]] = None


class ChatroomApiMixin:
    def create_chatroom(
        self: HttpClient, chat: ChatroomInfo
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/chatrooms/create", chat)

    def destroy_chatroom(
        self: HttpClient, chat: ChatroomInfo
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/chatrooms/destroy", chat)

    def qry_chatroom_info(
        self: HttpClient,
        chat_id: str,
        with_members: bool,
        with_atts: bool,
        order: int,
        count: int,
    ) -> Tuple[Optional[ChatroomInfo], ApiCode, str, Optional[Exception]]:
        return self._get(
            f"/apigateway/chatrooms/info?chat_id={chat_id}&with_members={str(with_members).lower()}&with_atts={str(with_atts).lower()}&order={order}&count={count}",
            ChatroomInfo,
        )

    def set_chatroom_mute(
        self: HttpClient, chat_id: str, is_mute: bool
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        mute = 1 if is_mute else 0
        return self._post(
            "/apigateway/chatrooms/chrmmute/set", ChatroomInfo(chat_id=chat_id, is_mute=mute)
        )

    def chrm_members_exists(
        self: HttpClient, req: ChrmMemberIds
    ) -> Tuple[Optional[ChrmMembersExistResp], ApiCode, str, Optional[Exception]]:
        return self.http_call("POST", "/apigateway/chatrooms/members/exist", req, ChrmMembersExistResp)

    def add_chrm_mute_members(
        self: HttpClient, req: ChrmBanUserReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/chatrooms/mutemembers/add", req)

    def del_chrm_mute_members(
        self: HttpClient, req: ChrmBanUserReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/chatrooms/mutemembers/del", req)

    def qry_chrm_mute_members(
        self: HttpClient, chat_id: str, offset: str, limit: int
    ) -> Tuple[Optional[ChrmBanUsers], ApiCode, str, Optional[Exception]]:
        return self._get(
            f"/apigateway/chatrooms/mutemembers/query?chat_id={chat_id}&offset={offset}&limit={limit}",
            ChrmBanUsers,
        )

    def add_chrm_global_mute_members(
        self: HttpClient, req: ChrmBanUserReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/chatrooms/globalmutemembers/add", req)

    def del_chrm_global_mute_members(
        self: HttpClient, req: ChrmBanUserReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/chatrooms/globalmutemembers/del", req)

    def qry_chrm_global_mute_members(
        self: HttpClient, offset: str, limit: int
    ) -> Tuple[Optional[ChrmBanUsers], ApiCode, str, Optional[Exception]]:
        return self._get(
            f"/apigateway/chatrooms/globalmutemembers/query?offset={offset}&limit={limit}",
            ChrmBanUsers,
        )

    def add_chrm_ban_members(
        self: HttpClient, req: ChrmBanUserReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/chatrooms/banmembers/add", req)

    def del_chrm_ban_members(
        self: HttpClient, req: ChrmBanUserReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/chatrooms/banmembers/del", req)

    def qry_chrm_ban_members(
        self: HttpClient, chat_id: str, offset: str, limit: int
    ) -> Tuple[Optional[ChrmBanUsers], ApiCode, str, Optional[Exception]]:
        return self._get(
            f"/apigateway/chatrooms/banmembers/query?chat_id={chat_id}&offset={offset}&limit={limit}",
            ChrmBanUsers,
        )

    def add_chrm_allow_members(
        self: HttpClient, req: ChrmBanUserReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/chatrooms/allowmembers/add", req)

    def del_chrm_allow_members(
        self: HttpClient, req: ChrmBanUserReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/chatrooms/allowmembers/del", req)

    def qry_chrm_allow_members(
        self: HttpClient, chat_id: str, offset: str, limit: int
    ) -> Tuple[Optional[ChrmBanUsers], ApiCode, str, Optional[Exception]]:
        return self._get(
            f"/apigateway/chatrooms/allowmembers/query?chat_id={chat_id}&offset={offset}&limit={limit}",
            ChrmBanUsers,
        )

    def add_chrm_atts(
        self: HttpClient, req: ChatroomAtts
    ) -> Tuple[Optional[ChatroomAttsResp], ApiCode, str, Optional[Exception]]:
        return self.http_call("POST", "/apigateway/chatrooms/atts/add", req, ChatroomAttsResp)

    def del_chrm_atts(
        self: HttpClient, req: ChatroomAtts
    ) -> Tuple[Optional[ChatroomAttsResp], ApiCode, str, Optional[Exception]]:
        return self.http_call("POST", "/apigateway/chatrooms/atts/del", req, ChatroomAttsResp)

    def qry_chrm_atts(
        self: HttpClient, req: ChatroomAttsReq
    ) -> Tuple[Optional[ChatroomInfo], ApiCode, str, Optional[Exception]]:
        return self.http_call("POST", "/apigateway/chatrooms/atts/qry", req, ChatroomInfo)

    def list_chrm_atts(
        self: HttpClient, chat_id: str
    ) -> Tuple[Optional[ChatroomInfo], ApiCode, str, Optional[Exception]]:
        return self._get(f"/apigateway/chatrooms/atts/list?chat_id={chat_id}", ChatroomInfo)
