"""Push / User tags API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from juggleimsdk._base import HttpClient
from juggleimsdk.mute import UserIds
from juggleimsdk.util import ApiCode


@dataclass
class UserTag:
    user_id: str = ""
    tags: Optional[List[str]] = None


@dataclass
class UserTagsPayload:
    user_tags: Optional[List[UserTag]] = None


@dataclass
class PushCondition:
    tags_and: Optional[List[str]] = None
    tags_or: Optional[List[str]] = None


@dataclass
class PushMsgBody:
    msg_type: str = ""
    msg_content: str = ""


@dataclass
class PushNotification:
    title: str = ""
    push_text: str = ""


@dataclass
class PushPayload:
    from_user_id: str = ""
    condition: Optional[PushCondition] = None
    msg_body: Optional[PushMsgBody] = None
    notification: Optional[PushNotification] = None


@dataclass
class PushResp:
    push_id: str = ""


class PushApiMixin:
    def qry_user_tags(
        self: HttpClient, user_ids: List[str]
    ) -> Tuple[Optional[UserTagsPayload], ApiCode, str, Optional[Exception]]:
        if not user_ids:
            return UserTagsPayload(), ApiCode.SUCCESS, "", None
        params = "&".join(f"user_id={uid}" for uid in user_ids)
        return self._get(f"/apigateway/usertags/query?{params}", UserTagsPayload)

    def add_user_tags(
        self: HttpClient, req: UserTagsPayload
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/usertags/add", req)

    def del_user_tags(
        self: HttpClient, req: UserTagsPayload
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/usertags/del", req)

    def clear_user_tags(
        self: HttpClient, user_ids: List[str]
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/usertags/clear", UserIds(user_ids=user_ids))

    def push_with_tags(
        self: HttpClient, req: PushPayload
    ) -> Tuple[Optional[PushResp], ApiCode, str, Optional[Exception]]:
        return self.http_call("POST", "/apigateway/push", req, PushResp)
