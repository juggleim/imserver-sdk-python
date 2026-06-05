"""Conversation API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

from juggleimsdk._base import HttpClient
from juggleimsdk.util import ApiCode


@dataclass
class Conversation:
    id: str = ""
    user_id: str = ""
    target_id: str = ""
    channel_type: int = 0
    sub_channel: str = ""
    time: int = 0


@dataclass
class Conversations:
    user_id: str = ""
    items: Optional[List[Conversation]] = None
    is_finished: bool = False


@dataclass
class UndisturbConverItem:
    target_id: str = ""
    channel_type: int = 0
    undisturb_type: int = 0


@dataclass
class UndisturbConversReq:
    user_id: str = ""
    items: Optional[List[UndisturbConverItem]] = None


@dataclass
class TopConverReqItem:
    target_id: str = ""
    channel_type: int = 0
    is_top: bool = False


@dataclass
class TopConversReq:
    user_id: str = ""
    items: Optional[List[TopConverReqItem]] = None


@dataclass
class TagConversReq:
    user_id: str = ""
    tag: str = ""
    tag_name: str = ""
    convers: Optional[List[Conversation]] = None


class ConversationApiMixin:
    def clear_unread(
        self: HttpClient, convers: Conversations
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/convers/clearunread", convers)

    def qry_global_convers(
        self: HttpClient,
        start_time: int,
        count: int,
        target_id: Optional[str] = None,
        channel_type: Optional[int] = None,
    ) -> Tuple[Optional[Conversations], ApiCode, str, Optional[Exception]]:
        return self.qry_global_convers_with_exclude(
            start_time, count, target_id, channel_type, None
        )

    def qry_global_convers_with_exclude(
        self: HttpClient,
        start_time: int,
        count: int,
        target_id: Optional[str] = None,
        channel_type: Optional[int] = None,
        exclude_user_ids: Optional[List[str]] = None,
    ) -> Tuple[Optional[Conversations], ApiCode, str, Optional[Exception]]:
        if count < 0 or count > 50:
            count = 50
        url_path = f"/apigateway/globalconvers/query?start={start_time}&count={count}"
        if target_id:
            url_path += f"&target_id={target_id}"
        if channel_type is not None and channel_type > 0:
            url_path += f"&channel_type={channel_type}"
        for uid in exclude_user_ids or []:
            url_path += f"&exclude_user_id={uid}"
        return self._get(url_path, Conversations)

    def add_conversation(
        self: HttpClient, conver: Conversation
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/convers/add", conver)

    def del_conversation(
        self: HttpClient, convers: Conversations
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/convers/del", convers)

    def undisturb_convers(
        self: HttpClient, req: UndisturbConversReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/convers/undisturb", req)

    def top_conversations(
        self: HttpClient, req: TopConversReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/convers/top", req)

    def qry_convers(
        self: HttpClient, user_id: str, start_time: int, count: int, order: int
    ) -> Tuple[Optional[Conversations], ApiCode, str, Optional[Exception]]:
        if count < 0 or count > 100:
            count = 100
        return self._get(
            f"/apigateway/convers/query?user_id={user_id}&start={start_time}&count={count}&order={order}",
            Conversations,
        )

    def tag_convers(
        self: HttpClient, req: TagConversReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/convers/tags/add", req)

    def un_tag_convers(
        self: HttpClient, req: TagConversReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/convers/tags/del", req)
