"""Assembled SDK client."""

from juggleimsdk._base import DEFAULT_API_URL, HttpClient
from juggleimsdk.app import AppApiMixin
from juggleimsdk.binddevice import BindDeviceApiMixin
from juggleimsdk.bot import BotApiMixin
from juggleimsdk.chatroom import ChatroomApiMixin
from juggleimsdk.conversation import ConversationApiMixin
from juggleimsdk.friend import FriendApiMixin
from juggleimsdk.group import GroupApiMixin
from juggleimsdk.hismsg import HisMsgApiMixin
from juggleimsdk.message import MessageApiMixin
from juggleimsdk.moment import MomentApiMixin
from juggleimsdk.mute import MuteApiMixin
from juggleimsdk.publicchannel import PublicChannelApiMixin
from juggleimsdk.push import PushApiMixin
from juggleimsdk.sensitive import SensitiveApiMixin
from juggleimsdk.user import UserApiMixin


class JuggleIMSdk(
    HttpClient,
    UserApiMixin,
    MessageApiMixin,
    GroupApiMixin,
    BotApiMixin,
    AppApiMixin,
    SensitiveApiMixin,
    PushApiMixin,
    PublicChannelApiMixin,
    MuteApiMixin,
    MomentApiMixin,
    HisMsgApiMixin,
    FriendApiMixin,
    ConversationApiMixin,
    ChatroomApiMixin,
    BindDeviceApiMixin,
):
    """JuggleIM Server API client."""


def new_juggle_im_sdk(appkey: str, secret: str, api_url: str = DEFAULT_API_URL) -> JuggleIMSdk:
    return JuggleIMSdk(appkey, secret, api_url)
