# JuggleIM Server Python SDK

Python 3 SDK for JuggleIM Server API, ported from [imserver-sdk-go](https://github.com/juggleim/imserver-sdk-go).

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from juggleimsdk import User, new_juggle_im_sdk

imsdk = new_juggle_im_sdk("appkey", "appsecret", "https://api.juggle.im")

resp, code, trace_id, err = imsdk.register(User(user_id="userid1"))
if err:
    print(f"error: {err}, code={code}, trace={trace_id}")
else:
    print(f"user_id={resp.user_id}, token={resp.token}")
```

## API Coverage

The SDK mirrors the Go SDK and includes:

- User management (register, ban, block, online status, etc.)
- Message sending (private, group, chatroom, broadcast, etc.)
- Group management
- Conversation management
- History messages
- Chatroom
- Friends
- Moments
- Public channels
- Push / user tags
- Sensitive words
- Bots
- Bind devices
- Global mute

## Requirements

- Python 3.8+
- No third-party dependencies (uses stdlib only)
