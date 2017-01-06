import hashlib
import hmac
import json

from pip._vendor import requests

API_URL = 'https://demo-api2.inplat.ru'
API_KEY = 'F5aPOR2Zm3vHFQXVBjLgpnub'
SECRET_WORD = b'B1BUnfwEE2mAUK4D'

payment_params = {
    'method': 'init',
    'pay_type': 'mc',
    'pay_params': {
        'msidn': 79265327000
    },
    'params': {
        'account': 'test',
        'sum': 1023,
        'email': 'vasya.pupkin@pochta.ru',
        'details': 'Оплата заказа No123',
        'address': 'Москва',
    }
}

payment_params = json.dumps(payment_params).encode('utf-8')
print(payment_params)

sign = hmac.new(SECRET_WORD, msg=payment_params, digestmod=hashlib.sha256).hexdigest()
print(sign)


API_PARAMS = {
    'apikey': API_KEY,
    'sign': sign,
}

r = requests.get(API_URL, params=API_PARAMS)
decode = r.json()
print(decode)