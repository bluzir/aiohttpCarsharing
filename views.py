import aiohttp_jinja2 as aiohttp_jinja2
from aiohttp import web

import settings
from inplat_wrapper.api import InplatClient

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


async def ride_start(request):
    car_id = int(request.match_info['car_id'])
    # Bussiness logic for car
    return web.json_response({'success': 'true', 'ride_start_time': 'time', 'car_id': car_id})


def ride_end(request):
    return web.Response(text='Ride end!')


def reservation_start(request):
    return web.Response(text='Reservation start!')


def reservation_end(request):
    return web.Response(text='Reservation end!')

async def cars_list(request):
    return web.json_response(data)

async def cars_detail(request):
    car_id = int(request.match_info['car_id'])
    local_data = data['cars'][car_id]
    return web.json_response(local_data)


@aiohttp_jinja2.template('payment_form.html')
async def payment_form(request):
    user_id = 123123 # Get user id from session
    return {'user_id': user_id}


@aiohttp_jinja2.template('payment_form.html')
async def do_payment(request):
    data = await request.post()
    try:
        card_number = data['card-number']
        year = data['year']
        month = data['month']
        cvv = data['cvv']
        card_holder = data['card-holder']
        user_id = data['user-id']
        client = InplatClient()
        pay_params = {
            'pan': card_number,
            'expire_month': month,
            'expire_year': year,
            'cvv': cvv,
            'cardholder_name': card_holder,
        }
        params = {
            'sum': 1111,
            'account': '1231231',
        }
        response = client.init(pay_type='card',
                               client_id=user_id,
                               pay_params=pay_params,
                               params=params)
        if response['code'] != 0:
            return {'error': response['message']}
        else:
            return {'success': True, 'id': response['id'], 'url': response['id']}
    except KeyError:
        return {'error': 'Заполните все поля'}
    except Exception as e:
        return {'error': e}



class CarsListView(web.View):
    async def get(self):
        return await cars_list(self.request)


class CarsDetailView(web.View):
    async def get(self):
        return await cars_detail(self.request)


class RideStartView(web.View):
    async def get(self):
        return await ride_start(self.request)

    async def post(self):
        return await ride_start(self.request)


class PaymentView(web.View):
    async def get(self):
        return await payment_form(self.request)

    async def post(self):
        return await do_payment(self.request)
