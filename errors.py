# Я правда пытался сделать что-нибудь приличное
# Но пока что рабочее получилось сделать только вот так
from aiohttp import web


class _error:

    TOKEN_REQUIRED = 1
    INVALID_TOKEN = 2
    NO_CRYPTOGRAMA = 3
    INVALID_LOGIN = 4
    EMPTY_FIELD = 5

    errors = {
        1: {
            'ru': 'Требуется токен',
            'en': 'Token required',
        },
        2: {
            'ru': 'Неправильный токен',
            'en': 'Invalid token',
        },
        3: {
            'ru': 'Криптограмма не передана',
            'en': 'Cryptograma not passed'
        },
        4: {
            'ru': 'Неверный логин или пароль',
            'en': 'Wrond login or password'

        },
        5: {
            'ru': 'Заполнены не все поля',
            'en': 'Not all fields are filled'

        }

    }

    def error_response(self, error):
        error = self.errors[error]
        return web.json_response({'error': error['ru']})
