import asyncio

import functools

from aiohttp import web
from aiohttp_session import get_session

from errors import _error

from models.user import User

# Simple decorator that add information about session to template context



def session_decorator():
    def wrapper(func):
        @asyncio.coroutine
        @functools.wraps(func)
        def wrapped(request):
            session = yield from get_session(request)
            func_context = yield from func(request)  # get context from wrapped func
            session_context = {'session': session}
            return {**func_context, **session_context}
        return wrapped
    return wrapper


# Decorator for html views that check authorization
# and add information about it to the template context
def token_required():
    def wrapper(func):
        @asyncio.coroutine
        @functools.wraps(func)
        def wrapped(request):
            session = yield from get_session(request)
            func_context = yield from func(request)  # get context from wrapped func
            if 'auth_token' in session:
                user_id = User.decode_auth_token(session['auth_token'])
                if user_id:
                    session_context = {'token': session['auth_token'], 'session': session}
                    return {**func_context, **session_context}
            else:
                return web.HTTPFound('/login/')
        return wrapped
    return wrapper


# Decorator for API controllers that checks if auth_token passed and valid
def check_token():
    def wrapper(func):
        @asyncio.coroutine
        @functools.wraps(func)
        def wrapped(request):
            if 'token' in request.GET:
                user = User.get_user_by_token(request.GET['token'])
                if user:
                    return func(request, user)
                else:
                    return _error.error_response(_error, _error.INVALID_TOKEN)

            return _error.error_response(_error, _error.TOKEN_REQUIRED)
        return wrapped
    return wrapper