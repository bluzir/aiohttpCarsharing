import requests


class WialonException:
    pass


class WialonClient:

    # Default host settings
    DEFAULT_HOST = 'https://hst-api.wialon.com/{}'
    API_URL_POSTFIX = 'wialon/ajax.html'

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
        self.authenticated = False

        if not token:
            raise Exception

    def login(self):
        login_params = {"token": self.token}

        return self.request(
            method='token/login',
            params=login_params,)

    def get_profile_info(self, detail=False):
        profile_params = {"type": 1 if not detail else 2}

        return self.request(
            method='core/get_account_data',
            params=profile_params,
        )

    def get_fuel_consumption(self, unit_id):
        fuel_params = {"itemId": unit_id}

        return self.request(
            method='unit/get_fuel_settings',
            params=fuel_params,
        )

    def get_sensors_values_by_id(self, unit_id):
        unit_params = {
            'source': '',
            'indexFrom': '',
            'indexTo': '',
            'unitId': unit_id,
            'sensorId': '',
            'width': ''
        }

        return self.request(
            method='unit/calc_sensors',
            params=unit_params,
        )

    def execute_command_by_name(self, unit_id, name, params=None):
        command_params = {
            'itemId': unit_id,
            'commandName': name,
            'linkType': '',
            'param': params,
            'timeout': '',
            'flags': ''
        }

        return self.request(
            method='unit/exec_cmd',
            params=command_params,
        )

    def request(self, method, params, **kwargs):
        url = self.DEFAULT_HOST.format(self.API_URL_POSTFIX)
        par = {
            'svc': method,
            'params': params
        }

        response = requests.get(
            url=url,
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
    client.authenticated = True