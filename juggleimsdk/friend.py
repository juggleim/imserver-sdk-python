"""Friend API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

from juggleimsdk._base import HttpClient
from juggleimsdk.util import ApiCode


@dataclass
class FriendItem:
    user_id: str = ""
    friend_id: str = ""
    display_name: str = ""


@dataclass
class FriendIds:
    user_id: str = ""
    friend_ids: Optional[List[str]] = None
    friends: Optional[List[FriendItem]] = None


@dataclass
class FriendsResp:
    items: Optional[List[FriendItem]] = None
    offset: str = ""


class FriendApiMixin:
    def add_friends(
        self: HttpClient, friend_ids: FriendIds
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/friends/add", friend_ids)

    def del_friends(
        self: HttpClient, friend_ids: FriendIds
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/friends/del", friend_ids)

    def qry_friends(
        self: HttpClient, user_id: str, limit: int, offset: str, order: int
    ) -> Tuple[Optional[FriendsResp], ApiCode, str, Optional[Exception]]:
        return self._get(
            f"/apigateway/friends/query?user_id={user_id}&limit={limit}&offset={offset}&order={order}",
            FriendsResp,
        )

    def set_friend_display_name(
        self: HttpClient, item: FriendItem
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/friends/setdisplayname", item)
