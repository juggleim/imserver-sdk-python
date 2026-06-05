"""Example usage of JuggleIM Python SDK."""

from juggleimsdk import User, new_juggle_im_sdk


def main() -> None:
    imsdk = new_juggle_im_sdk("appkey", "appsecret", "https://api.juggle.im")

    resp, code, trace, err = imsdk.register(User(user_id="userid1"))
    print(resp, code, trace, err)


if __name__ == "__main__":
    main()
