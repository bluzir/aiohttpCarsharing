import hashlib
import hmac


def create_sign(secret, message):
    """
    Returns HMAC-SHA256 (api_secret, request body)
    """
    sign = hmac.new(secret, msg=message, digestmod=hashlib.sha256).hexdigest()
    return sign
