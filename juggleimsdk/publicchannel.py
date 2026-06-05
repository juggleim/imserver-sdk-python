"""Public channel API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

from juggleimsdk._base import HttpClient
from juggleimsdk.util import ApiCode


@dataclass
class PublicChannelInfo:
    channel_id: str = ""
    channel_name: str = ""
    channel_portrait: str = ""
    creator_id: str = ""
    created_time: int = 0
    updated_time: int = 0


@dataclass
class PublicChannelMemberIds:
    channel_id: str = ""
    member_ids: Optional[List[str]] = None


@dataclass
class PublicChannelMember:
    member_id: str = ""
    created_time: int = 0


@dataclass
class PublicChannelMembers:
    members: Optional[List[PublicChannelMember]] = None
    offset: str = ""
    limit: int = 0


class PublicChannelApiMixin:
    def create_public_channel(
        self: HttpClient, channel: PublicChannelInfo
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/publicchannel/create", channel)

    def update_public_channel(
        self: HttpClient, channel: PublicChannelInfo
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/publicchannel/update", channel)

    def destroy_public_channel(
        self: HttpClient, channel: PublicChannelInfo
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/publicchannel/destroy", channel)

    def subscribe_public_channel(
        self: HttpClient, req: PublicChannelMemberIds
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/publicchannel/subscribe", req)

    def unsubscribe_public_channel(
        self: HttpClient, req: PublicChannelMemberIds
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/publicchannel/unsubscribe", req)

    def qry_public_channel_members(
        self: HttpClient, channel_id: str, offset: str, limit: int
    ) -> Tuple[Optional[PublicChannelMembers], ApiCode, str, Optional[Exception]]:
        return self._get(
            f"/apigateway/publicchannel/members/list?channel_id={channel_id}&offset={offset}&limit={limit}",
            PublicChannelMembers,
        )
