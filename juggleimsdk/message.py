"""Message API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

from juggleimsdk._base import HttpClient
from juggleimsdk.user import User
from juggleimsdk.util import ApiCode


class MentionType:
    ALL = "mention_all"
    SOMEONE = "mention_someone"
    ALL_SOMEONE = "mention_all_someone"


@dataclass
class MentionInfo:
    mention_type: str = ""
    target_users: Optional[List[User]] = None
    target_user_ids: Optional[List[str]] = None


@dataclass
class ReferMsg:
    msg_id: str = ""
    sender_id: str = ""
    target_id: str = ""
    channel_type: int = 0
    msg_type: str = ""
    msg_time: int = 0
    msg_content: str = ""


@dataclass
class PushData:
    push_title: str = ""
    push_text: str = ""
    push_extra: str = ""
    push_level: int = 0


@dataclass
class Message:
    sender_id: str = ""
    target_id: str = ""
    receiver_id: str = ""
    target_ids: Optional[List[str]] = None
    to_user_ids: Optional[List[str]] = None
    msg_type: str = ""
    msg_content: str = ""
    life_time: int = 0
    life_time_after_read: int = 0
    is_storage: Optional[bool] = None
    is_count: Optional[bool] = None
    is_notify_sender: Optional[bool] = None
    is_state: Optional[bool] = None
    is_cmd: Optional[bool] = None
    mention_info: Optional[MentionInfo] = None
    refer_msg: Optional[ReferMsg] = None
    push_data: Optional[PushData] = None
    msg_id: Optional[str] = None


@dataclass
class TargetConver:
    target_id: str = ""
    channel_type: int = 0


@dataclass
class SendGrpCastMsgReq:
    sender_id: str = ""
    target_id: str = ""
    msg_type: str = ""
    msg_content: str = ""
    target_convers: Optional[List[TargetConver]] = None


@dataclass
class SendBrdCastMsgReq:
    sender_id: str = ""
    msg_type: str = ""
    msg_content: str = ""
    is_storage: Optional[bool] = None


@dataclass
class MarkReadReq:
    user_id: str = ""
    target_id: str = ""
    channel_type: int = 0
    msg_ids: Optional[List[str]] = None


@dataclass
class StreamMsg:
    msg_id: str = ""
    from_id: str = ""
    target_id: str = ""
    partial_content: str = ""
    seq: int = 0
    is_finished: bool = False


@dataclass
class SendMsgRespItem:
    target_id: str = ""
    msg_id: str = ""


class MessageApiMixin:
    def send_private_msg(
        self: HttpClient, msg: Message
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/messages/private/send", msg)

    def send_system_msg(
        self: HttpClient, msg: Message
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/messages/system/send", msg)

    def send_group_msg(
        self: HttpClient, msg: Message
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/messages/group/send", msg)

    def send_chatroom_msg(
        self: HttpClient, msg: Message
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/messages/chatroom/send", msg)

    def send_chatroom_brd_msg(
        self: HttpClient, msg: Message
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/messages/chatroom/broadcast", msg)

    def send_group_cast_msg(
        self: HttpClient, req: SendGrpCastMsgReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/messages/groupcast/send", req)

    def send_broad_cast_msg(
        self: HttpClient, req: SendBrdCastMsgReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/messages/broadcast/send", req)

    def send_public_channel_msg(
        self: HttpClient, msg: Message
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/messages/publicchannel/send", msg)

    def mark_read(
        self: HttpClient, req: MarkReadReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/messages/markread", req)

    def send_private_stream_msg(
        self: HttpClient, msg: StreamMsg
    ) -> Tuple[Optional[SendMsgRespItem], ApiCode, str, Optional[Exception]]:
        return self.http_call(
            "POST", "/apigateway/messages/private/stream/send", msg, SendMsgRespItem
        )

    def send_private_msg_with_resp(
        self: HttpClient, msg: Message
    ) -> Tuple[Optional[List[SendMsgRespItem]], ApiCode, str, Optional[Exception]]:
        return self.http_call(
            "POST",
            "/apigateway/messages/private/send",
            msg,
            resp_cls=List[SendMsgRespItem],  # type: ignore[arg-type]
            resp_is_list=True,
        )

    def send_system_msg_with_resp(
        self: HttpClient, msg: Message
    ) -> Tuple[Optional[List[SendMsgRespItem]], ApiCode, str, Optional[Exception]]:
        return self.http_call(
            "POST",
            "/apigateway/messages/system/send",
            msg,
            resp_cls=List[SendMsgRespItem],  # type: ignore[arg-type]
            resp_is_list=True,
        )

    def send_group_msg_with_resp(
        self: HttpClient, msg: Message
    ) -> Tuple[Optional[List[SendMsgRespItem]], ApiCode, str, Optional[Exception]]:
        return self.http_call(
            "POST",
            "/apigateway/messages/group/send",
            msg,
            resp_cls=List[SendMsgRespItem],  # type: ignore[arg-type]
            resp_is_list=True,
        )

    def send_chatroom_msg_with_resp(
        self: HttpClient, msg: Message
    ) -> Tuple[Optional[List[SendMsgRespItem]], ApiCode, str, Optional[Exception]]:
        return self.http_call(
            "POST",
            "/apigateway/messages/chatroom/send",
            msg,
            resp_cls=List[SendMsgRespItem],  # type: ignore[arg-type]
            resp_is_list=True,
        )

    def send_public_channel_msg_with_resp(
        self: HttpClient, msg: Message
    ) -> Tuple[Optional[List[SendMsgRespItem]], ApiCode, str, Optional[Exception]]:
        return self.http_call(
            "POST",
            "/apigateway/messages/publicchannel/send",
            msg,
            resp_cls=List[SendMsgRespItem],  # type: ignore[arg-type]
            resp_is_list=True,
        )
