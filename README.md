<div align="center">

# JuggleIM Server Python SDK

**A dependency-free Python client for the JuggleIM Server REST API.**

[![CI](https://img.shields.io/github/actions/workflow/status/juggleim/imserver-sdk-python/ci.yml?branch=master&style=flat-square&label=CI)](https://github.com/juggleim/imserver-sdk-python/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?style=flat-square&logo=python&logoColor=white)](./pyproject.toml)
[![License](https://img.shields.io/github/license/juggleim/imserver-sdk-python?style=flat-square)](./LICENSE)
[![Stars](https://img.shields.io/github/stars/juggleim/imserver-sdk-python?style=flat-square)](https://github.com/juggleim/imserver-sdk-python/stargazers)

**English** · **[简体中文](./README_zh.md)**

[Website](https://www.juggle.im/) ·
[Documentation](https://www.juggle.im/docs/guide/intro/) ·
[Server API](https://www.juggle.im/docs/server/api/) ·
[IM Server](https://github.com/juggleim/im-server)

</div>

---

`imserver-sdk-python` lets a trusted Python backend call JuggleIM server APIs without
reimplementing request signing, serialization, and response mapping. It uses only the Python
standard library and is intended for server-side applications.

> [!IMPORTANT]
> Your app secret grants privileged server API access. Never embed it in a mobile, desktop,
> browser, or other client application.

## API coverage

- Users: registration, profiles, online status, bans, blocks, devices, and settings
- Messages: private, group, chatroom, broadcast, recall, and history
- Groups, conversations, chatrooms, friends, moments, and public channels
- Push tags, sensitive words, bots, device binding, and global mute controls

For other server languages, see the [Go](https://github.com/juggleim/imserver-sdk-go) and
[Java](https://github.com/juggleim/imserver-sdk-java) SDKs.

## Requirements

- Python 3.10 or newer
- A running [JuggleIM server](https://github.com/juggleim/im-server)
- An app key and app secret created in the JuggleIM admin console

## Install from source

The package is not currently published on PyPI. Install the tagged source directly:

```bash
python -m pip install "git+https://github.com/juggleim/imserver-sdk-python.git@v1.0.0"
```

For local development:

```bash
git clone https://github.com/juggleim/imserver-sdk-python.git
cd imserver-sdk-python
python -m pip install -e .
```

## Quick start

Set server credentials outside your source code:

```bash
export JUGGLEIM_APP_KEY="your-app-key"
export JUGGLEIM_APP_SECRET="your-app-secret"
export JUGGLEIM_API_URL="http://127.0.0.1:9001"
```

Register a user:

```python
import os

from juggleimsdk import User, new_juggle_im_sdk

sdk = new_juggle_im_sdk(
    os.environ["JUGGLEIM_APP_KEY"],
    os.environ["JUGGLEIM_APP_SECRET"],
    os.environ.get("JUGGLEIM_API_URL", "http://127.0.0.1:9001"),
)

user, code, trace_id, error = sdk.register(
    User(user_id="alice", nickname="Alice")
)

if error:
    raise RuntimeError(f"register failed: code={code}, trace_id={trace_id}: {error}")

print(user.user_id, user.token)
```

SDK methods return `(data, code, trace_id, error)` when the endpoint returns data, or
`(code, trace_id, error)` for operations without a response body. Always log the trace ID when
reporting a failed request.

See [`examples/main.py`](./examples/main.py) and the
[Server API reference](https://www.juggle.im/docs/server/api/) for more operations.

## Development

The test suite does not call a live JuggleIM server:

```bash
python -m unittest discover -s tests -v
python -m build
```

## Community and support

- [Ask a question](https://github.com/orgs/juggleim/discussions)
- [Report a bug](https://github.com/juggleim/imserver-sdk-python/issues/new)
- [Contribute](https://github.com/juggleim/.github/blob/main/CONTRIBUTING.md)

## License

[Apache License 2.0](./LICENSE)
