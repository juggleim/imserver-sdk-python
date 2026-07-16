<div align="center">

# JuggleIM 服务端 Python SDK

**零第三方运行时依赖的 JuggleIM Server REST API Python 客户端。**

[![CI](https://img.shields.io/github/actions/workflow/status/juggleim/imserver-sdk-python/ci.yml?branch=master&style=flat-square&label=CI)](https://github.com/juggleim/imserver-sdk-python/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?style=flat-square&logo=python&logoColor=white)](./pyproject.toml)
[![License](https://img.shields.io/github/license/juggleim/imserver-sdk-python?style=flat-square)](./LICENSE)
[![Stars](https://img.shields.io/github/stars/juggleim/imserver-sdk-python?style=flat-square)](https://github.com/juggleim/imserver-sdk-python/stargazers)

**[English](./README.md)** · **简体中文**

[官网](https://www.juggle.im/) ·
[文档](https://www.juggle.im/docs/guide/intro/) ·
[服务端 API](https://www.juggle.im/docs/server/api/) ·
[IM Server](https://github.com/juggleim/im-server)

</div>

---

`imserver-sdk-python` 帮助可信任的 Python 业务后端调用 JuggleIM 服务端 API，无需重复实现请求签名、序列化和响应映射。SDK 只使用 Python 标准库，并且仅适用于服务端应用。

> [!IMPORTANT]
> App Secret 拥有服务端 API 的高权限。绝不能把它嵌入移动端、桌面端、浏览器或其他客户端应用。

## API 覆盖

- 用户：注册、资料、在线状态、封禁、黑名单、设备和设置
- 消息：单聊、群聊、聊天室、广播、撤回和历史消息
- 群组、会话、聊天室、好友、朋友圈和公众频道
- 推送标签、敏感词、机器人、设备绑定和全局禁言

其他服务端语言可查看 [Go](https://github.com/juggleim/imserver-sdk-go) 和
[Java](https://github.com/juggleim/imserver-sdk-java) SDK。

## 环境要求

- Python 3.10 或更高版本
- 正在运行的 [JuggleIM 服务](https://github.com/juggleim/im-server)
- 通过 JuggleIM 管理控制台创建的 App Key 和 App Secret

## 从源码安装

该软件包目前尚未发布到 PyPI，可直接安装带版本标签的源码：

```bash
python -m pip install "git+https://github.com/juggleim/imserver-sdk-python.git@v1.0.0"
```

本地开发：

```bash
git clone https://github.com/juggleim/imserver-sdk-python.git
cd imserver-sdk-python
python -m pip install -e .
```

## 快速开始

将服务端凭据保存在源码之外：

```bash
export JUGGLEIM_APP_KEY="your-app-key"
export JUGGLEIM_APP_SECRET="your-app-secret"
export JUGGLEIM_API_URL="http://127.0.0.1:9001"
```

注册一个用户：

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

有响应数据的方法返回 `(data, code, trace_id, error)`；无响应体的操作返回
`(code, trace_id, error)`。反馈请求失败时，请始终附带 trace ID。

更多操作请查看 [`examples/main.py`](./examples/main.py) 和
[服务端 API 文档](https://www.juggle.im/docs/server/api/)。

## 开发

测试不会调用真实的 JuggleIM 服务：

```bash
python -m unittest discover -s tests -v
python -m build
```

## 社区与支持

- [提问和讨论](https://github.com/orgs/juggleim/discussions)
- [反馈问题](https://github.com/juggleim/imserver-sdk-python/issues/new)
- [参与贡献](https://github.com/juggleim/.github/blob/main/CONTRIBUTING.md)

## 许可证

[Apache License 2.0](./LICENSE)
