import base64
import uuid


def generate_cookie_secret():
    return base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)


if __name__ == '__main__':
    generate_cookie_secret()