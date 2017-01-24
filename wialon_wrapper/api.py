import requests
import wialon


class WialonClient():
    # Default host settings
    DEFAULT_HOST = 'https://hst-api.wialon.com/wialon/ajax.html'

    # Errors codes
    errors = {
        1: 'Invalid session',
        2: 'Invalid service',
        3: 'Invalid result',
        4: 'Invalid input',
        5: 'Error performing request',
        6: 'Unknow error',
        7: 'Access denied',
        8: 'Invalid user name or password',
        9: 'Authorization server is unavailable, please try again later',
        1001: 'No message for selected interval',
        1002: 'Item with such unique property already exists',
        1003: 'Only one request of given time is allowed at the moment'
    }

    def __init__(self, token=None):
        self.token = token

        if not token:
            self.auth()

    def login(self):
        login_params = {
            "token": self.token,
        }

        return self.request(
            method='token/login',
            params=login_params,)

    def request(self, method, params):
        par = {
            'svc': method,
            'params': params
        }

        response = requests.get(
            url=self.DEFAULT_HOST,
            params=par,
        )

        decoded = response.json()

        if 'error' not in decoded:
            return decoded
        else:
            error = decoded['error']
            print(self.errors[error])
            return False


client = WialonClient(
    token='2fe8024e0ab91aa6c8ed82717b71bddcECDC362358DF7D90986F5173D405CD0D42DE7B38'
)

if client.login():
    print('Login successful')