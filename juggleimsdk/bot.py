"""Bot API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from juggleimsdk._base import HttpClient
from juggleimsdk.user import UserRegResp
from juggleimsdk.util import ApiCode


@dataclass
class BotConf:
    bot_id: str = ""
    url: str = ""
    api_key: str = ""
    is_stream: bool = False


@dataclass
class BotSettings:
    only_mentioned: bool = False


@dataclass
class BotInfo:
    bot_id: str = ""
    nickname: str = ""
    portrait: str = ""
    bot_conf: Optional[BotConf] = None
    bot_settings: Optional[BotSettings] = None
    ext_fields: Optional[Dict[str, str]] = None
    updated_time: int = 0


class BotApiMixin:
    def register_bot(
        self: HttpClient, bot: BotInfo
    ) -> Tuple[Optional[UserRegResp], ApiCode, str, Optional[Exception]]:
        return self.http_call("POST", "/apigateway/bots/register", bot, UserRegResp)

    def update_bot(
        self: HttpClient, bot: BotInfo
    ) -> Tuple[ApiCode, str, Optional[Exception]]:
        return self._post("/apigateway/bots/update", bot)
