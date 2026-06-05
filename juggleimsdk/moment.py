"""Moment API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from juggleimsdk._base import HttpClient
from juggleimsdk.user import User
from juggleimsdk.util import ApiCode


@dataclass
class MomentMedia:
    type: str = ""
    url: str = ""
    snapshot_url: str = ""
    width: int = 0
    height: int = 0
    duration: int = 0


@dataclass
class MomentContent:
    text: str = ""
    medias: Optional[List[MomentMedia]] = None


@dataclass
class Moment:
    user_id: str = ""
    moment_id: str = ""
    title: str = ""
    content: Optional[MomentContent] = None
    content_brief: str = ""
    moment_time: int = 0
    updated_time: int = 0
    user_info: Optional[User] = None
    top_comments: Optional[List["Comment"]] = None
    reactions: Optional[List["MomentReaction"]] = None


@dataclass
class AddMomentResp:
    moment_id: str = ""
    moment_time: int = 0


@dataclass
class MomentIds:
    user_id: str = ""
    moment_ids: List[str] = field(default_factory=list)


@dataclass
class Moments:
    items: Optional[List[Moment]] = None
    is_finished: bool = False


@dataclass
class CommentContent:
    text: str = ""


@dataclass
class Comment:
    user_id: str = ""
    comment_id: str = ""
    moment_id: str = ""
    parent_comment_id: str = ""
    content: Optional[CommentContent] = None
    comment_time: int = 0
    updated_time: int = 0
    seq_no: int = 0
    parent_user_info: Optional[User] = None
    user_info: Optional[User] = None


@dataclass
class CommentResp:
    comment_id: str = ""
    comment_time: int = 0
    seq_no: int = 0
    user_info: Optional[User] = None
    parent_user_info: Optional[User] = None


@dataclass
class CommentIds:
    user_id: str = ""
    moment_id: str = ""
    comment_ids: List[str] = field(default_factory=list)


@dataclass
class Comments:
    items: Optional[List[Comment]] = None
    is_finished: bool = False


@dataclass
class MomentReaction:
    key: str = ""
    value: str = ""
    timestamp: int = 0
    user_info: Optional[User] = None


@dataclass
class ReactionReq:
    user_id: str = ""
    moment_id: str = ""
    reaction: Optional[MomentReaction] = None


@dataclass
class MomentReactions:
    items: Optional[List[MomentReaction]] = None
    is_finished: bool = False


class MomentApiMixin:
    def add_moment(
        self: HttpClient, moment: Moment
    ) -> Tuple[Optional[AddMomentResp], ApiCode, str, Optional[Exception]]:
        return self.http_call("POST", "/apigateway/moments/add", moment, AddMomentResp)

    def update_moment(
        self: HttpClient, moment: Moment
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/moments/update", moment)

    def del_moment(
        self: HttpClient, req: MomentIds
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/moments/del", req)

    def moment_info(
        self: HttpClient, moment_id: str
    ) -> Tuple[Optional[Moment], ApiCode, str, Optional[Exception]]:
        return self._get(f"/apigateway/moments/info?moment_id={moment_id}", Moment)

    def qry_moments(
        self: HttpClient, user_id: str, start_time: int, limit: int, order: int
    ) -> Tuple[Optional[Moments], ApiCode, str, Optional[Exception]]:
        return self._get(
            f"/apigateway/moments/list?user_id={user_id}&start={start_time}&limit={limit}&order={order}",
            Moments,
        )

    def add_reaction(
        self: HttpClient, req: ReactionReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/moments/reactions/add", req)

    def del_reaction(
        self: HttpClient, req: ReactionReq
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/moments/reactions/del", req)

    def qry_reactions(
        self: HttpClient, moment_id: str, start_time: int, limit: int, order: int
    ) -> Tuple[Optional[MomentReactions], ApiCode, str, Optional[Exception]]:
        return self._get(
            f"/apigateway/moments/reactions/list?moment_id={moment_id}&start={start_time}&limit={limit}&order={order}",
            MomentReactions,
        )

    def add_comment(
        self: HttpClient, comment: Comment
    ) -> Tuple[Optional[CommentResp], ApiCode, str, Optional[Exception]]:
        return self.http_call("POST", "/apigateway/moments/comments/add", comment, CommentResp)

    def update_comment(
        self: HttpClient, comment: Comment
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/moments/comments/update", comment)

    def del_comment(
        self: HttpClient, req: CommentIds
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/moments/comments/del", req)

    def qry_comments(
        self: HttpClient, moment_id: str, start_time: int, limit: int, order: int
    ) -> Tuple[Optional[Comments], ApiCode, str, Optional[Exception]]:
        return self._get(
            f"/apigateway/moments/comments/list?moment_id={moment_id}&start={start_time}&limit={limit}&order={order}",
            Comments,
        )
