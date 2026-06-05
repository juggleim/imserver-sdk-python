"""Group API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from juggleimsdk._base import HttpClient
from juggleimsdk.util import ApiCode


@dataclass
class GroupMembersReq:
    group_id: str = ""
    group_name: str = ""
    group_portrait: str = ""
    member_ids: Optional[List[str]] = None


@dataclass
class GroupSettings:
    hide_grp_msg: Optional[int] = None
    grp_msg_second_limiter: Optional[int] = None
    grp_msg_minute_limiter: Optional[int] = None
    grp_msg_hour_limiter: Optional[int] = None


@dataclass
class GroupInfo:
    group_id: str = ""
    group_name: str = ""
    group_portrait: str = ""
    is_mute: int = 0
    updated_time: int = 0
    ext_fields: Optional[Dict[str, str]] = None
    settings: Optional[GroupSettings] = None


@dataclass
class GroupMemberSettings:
    hide_grp_msg: Optional[int] = None


@dataclass
class SetGroupSettingReq:
    group_id: str = ""
    settings: Optional[GroupSettings] = None


@dataclass
class SetGroupMemberSettingReq:
    group_id: str = ""
    member_id: str = ""
    settings: Optional[GroupMemberSettings] = None


@dataclass
class GroupMemberUpdateReq:
    group_id: str = ""
    member_id: str = ""
    grp_display_name: str = ""
    ext_fields: Optional[Dict[str, str]] = None


@dataclass
class GroupMemberAllowReq:
    group_id: str = ""
    member_ids: Optional[List[str]] = None
    is_allow: int = 0


@dataclass
class GroupMember:
    member_id: str = ""
    is_mute: int = 0
    is_allow: int = 0
    grp_display_name: str = ""
    ext_fields: Optional[Dict[str, str]] = None


@dataclass
class GroupMembers:
    items: Optional[List[GroupMember]] = None
    offset: str = ""


@dataclass
class GroupMuteReq:
    group_id: str = ""
    is_mute: int = 0


@dataclass
class GroupMembersMuteReq:
    group_id: str = ""
    member_ids: Optional[List[str]] = None
    is_mute: int = 0
    mute_minute: int = 0


class GroupApiMixin:
    def create_group(
        self: HttpClient, group_members: GroupMembersReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/groups/add", group_members)

    def group_add_members(
        self: HttpClient, group_members: GroupMembersReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self.create_group(group_members)

    def group_del_members(
        self: HttpClient, group_members: GroupMembersReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/groups/members/del", group_members)

    def dissolve_group(
        self: HttpClient, group_id: str
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/groups/del", GroupInfo(group_id=group_id))

    def update_group(
        self: HttpClient, grp_info: GroupInfo
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/groups/update", grp_info)

    def qry_group_info(
        self: HttpClient, grp_id: str
    ) -> Tuple[Optional[GroupInfo], ApiCode, str, Optional[Exception]]:
        return self._get(f"/apigateway/groups/info?group_id={grp_id}", GroupInfo)

    def qry_group_members(
        self: HttpClient, grp_id: str, limit: int, offset: str
    ) -> Tuple[Optional[GroupMembers], ApiCode, str, Optional[Exception]]:
        return self._get(
            f"/apigateway/groups/members/query?group_id={grp_id}&limit={limit}&offset={offset}",
            GroupMembers,
        )

    def group_members_by_ids(
        self: HttpClient, group_members: GroupMembersReq
    ) -> Tuple[Optional[GroupMembers], ApiCode, str, Optional[Exception]]:
        return self.http_call(
            "POST", "/apigateway/groups/members/querybyids", group_members, GroupMembers
        )

    def group_member_update(
        self: HttpClient, req: GroupMemberUpdateReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/groups/members/update", req)

    def set_group_members_allow(
        self: HttpClient, grp_id: str, is_allow: int, member_ids: List[str]
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post(
            "/apigateway/groups/groupmemberallow/set",
            GroupMemberAllowReq(group_id=grp_id, is_allow=is_allow, member_ids=member_ids),
        )

    def set_group_member_settings(
        self: HttpClient, req: SetGroupMemberSettingReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/groups/members/settings/set", req)

    def set_group_mute(
        self: HttpClient, grp_id: str, is_mute: int
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post(
            "/apigateway/groups/groupmute/set", GroupMuteReq(group_id=grp_id, is_mute=is_mute)
        )

    def set_group_members_mute(
        self: HttpClient, grp_id: str, is_mute: int, member_ids: List[str]
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post(
            "/apigateway/groups/groupmembermute/set",
            GroupMembersMuteReq(group_id=grp_id, is_mute=is_mute, member_ids=member_ids),
        )

    def set_group_settings(
        self: HttpClient, req: SetGroupSettingReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/groups/settings/set", req)

    def get_group_settings(
        self: HttpClient, grp_id: str
    ) -> Tuple[Optional[GroupInfo], ApiCode, str, Optional[Exception]]:
        return self._get(f"/apigateway/groups/settings/get?group_id={grp_id}", GroupInfo)
