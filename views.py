import aiohttp_jinja2 as aiohttp_jinja2
from aiohttp import web

import settings

data = {
    'cars': [
        {
            'id': 0,
            'lat': 59.9258,
            'long': 30.2878,
            'model': 'Toyota Camry',
            'color': 'Красный',
            'year': '2012',
        },
        {
            'id': 1,
            'lat': 59.9301,
            'long': 30.3645,
            'model': 'Hyundai Solaris',
            'color': 'Черный',
            'year': '2014',
        },
        {
            'id': 2,
            'lat': 59.9101,
            'long': 30.3245,
            'model': 'Kia Ceed',
            'color': 'Красный',
            'year': '2016',
        },
        {
            'id': 3,
            'lat': 59.9426378,
            'long': 30.2260552,
            'model': 'Kia Ceed',
            'color': 'Белый',
            'year': '2015',
        },
    ]
}


def index(request):
    return web.Response(text='Hello Aiohttp!')


@aiohttp_jinja2.template('maps.html')
def maps(request):
        api_key = settings.GMAPS_API_KEY
        return {
            'api_key': api_key,
        }

def cars_list(request):
    return web.json_response(data)


def cars_detail(request):
    car_id = int(request.match_info['car_id'])
    local_data = data['cars'][car_id]
    return web.json_response(local_data)