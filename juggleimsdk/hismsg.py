"""History message API."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Dict, List, Optional, Tuple

from juggleimsdk._base import HttpClient
from juggleimsdk.util import ApiCode


class ChannelType(IntEnum):
    PRIVATE = 1
    GROUP = 2


@dataclass
class HisMsg:
    sender_id: str = ""
    target_id: str = ""
    receiver_id: str = ""
    channel_type: int = 0
    msg_id: str = ""
    msg_time: int = 0
    msg_type: str = ""
    msg_content: str = ""
    original_msg_type: str = ""
    original_msg_content: str = ""
    is_storage: Optional[bool] = None
    is_count: Optional[bool] = None


@dataclass
class HisMsgs:
    msgs: Optional[List[HisMsg]] = None
    is_finished: bool = False


@dataclass
class RecallMsgReq:
    from_id: str = ""
    target_id: str = ""
    channel_type: int = 0
    msg_id: str = ""
    msg_time: int = 0
    exts: Optional[Dict[str, str]] = None


@dataclass
class SimpleMsg:
    msg_id: str = ""
    msg_time: int = 0
    msg_read_index: int = 0


@dataclass
class DelMsgsReq:
    from_id: str = ""
    target_id: str = ""
    channel_type: int = 0
    del_scope: int = 0
    msgs: Optional[List[SimpleMsg]] = None


@dataclass
class CleanHisMsgsReq:
    from_id: str = ""
    target_id: str = ""
    channel_type: int = 0
    clean_time: int = 0
    clean_time_offset: int = 0
    clean_scope: int = 0
    sender_id: str = ""


@dataclass
class ModifyHisMsgReq:
    from_id: str = ""
    target_id: str = ""
    channel_type: int = 0
    msg_id: str = ""
    msg_type: str = ""
    msg_content: str = ""


class HisMsgApiMixin:
    def qry_his_msgs(
        self: HttpClient,
        user_id: str,
        target_id: str,
        channel_type: ChannelType,
        start_time: int,
        count: int,
        is_positive: bool,
    ) -> Tuple[Optional[HisMsgs], ApiCode, str, Optional[Exception]]:
        if count < 0 or count > 50:
            count = 50
        order = 1 if is_positive else 0
        return self._get(
            f"/apigateway/hismsgs/query?channel_type={int(channel_type)}&from_id={user_id}&target_id={target_id}&count={count}&order={order}&start={start_time}",
            HisMsgs,
        )

    def recall_msg(
        self: HttpClient, recall: RecallMsgReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/hismsgs/recall", recall)

    def del_msgs(
        self: HttpClient, del_msgs: DelMsgsReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/hismsgs/del", del_msgs)

    def qry_his_msgs_by_msg_ids(
        self: HttpClient,
        user_id: str,
        target_id: str,
        channel_type: ChannelType,
        msg_id: str,
    ) -> Tuple[Optional[HisMsgs], ApiCode, str, Optional[Exception]]:
        return self._get(
            f"/apigateway/hismsgs/querybymsgids?channel_type={int(channel_type)}&from_id={user_id}&target_id={target_id}&msg_id={msg_id}",
            HisMsgs,
        )

    def clean_his_msgs(
        self: HttpClient, req: CleanHisMsgsReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/hismsgs/clean", req)

    def modify_his_msg(
        self: HttpClient, req: ModifyHisMsgReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/hismsgs/modify", req)

    def import_his_msg(
        self: HttpClient, msg: HisMsg
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/hismsgs/import", msg)
