"""Example usage of JuggleIM Python SDK."""

import os

from juggleimsdk import User, new_juggle_im_sdk


def required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Set the {name} environment variable before running this example")
    return value


def main() -> None:
    imsdk = new_juggle_im_sdk(
        required_env("JUGGLEIM_APP_KEY"),
        required_env("JUGGLEIM_APP_SECRET"),
        os.environ.get("JUGGLEIM_API_URL", "http://127.0.0.1:9001"),
    )

    user, code, trace_id, error = imsdk.register(
        User(user_id="alice", nickname="Alice")
    )
    if error:
        raise RuntimeError(
            f"register failed: code={code}, trace_id={trace_id}: {error}"
        )
    print(user.user_id, user.token)


if __name__ == "__main__":
    main()
