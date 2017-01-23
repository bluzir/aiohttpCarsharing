import aiohttp_jinja2 as aiohttp_jinja2
from aiohttp import web

import settings


async def index(request):
    return web.Response(text='Hello Aiohttp!')


@aiohttp_jinja2.template('maps.html')
async def maps(request):
        api_key = settings.GMAPS_API_KEY
        return {
            'api_key': api_key,
        }

async def cars_list(request):
    data = {
        'cars': [
            {
                'id': 1,
                'lat': 59.9258,
                'long': 30.2878,
            },
            {
                'id': 2,
                'lat': 59.9301,
                'long': 30.3645,
            },
            {
                'id': 3,
                'lat': 59.9101,
                'long': 30.3245,
            },
        ]
    }
    return web.json_response(data)