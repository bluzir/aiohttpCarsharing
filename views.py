import json

import aiohttp_jinja2 as aiohttp_jinja2
from aiohttp import web
from aiohttp.web_exceptions import HTTPError, HTTPInternalServerError

import settings
from inplat_wrapper.api import InplatClient, InplatException

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

async def cars_list(request):
    return web.json_response(data)

async def cars_detail(request):
    car_id = int(request.match_info['car_id'])
    local_data = data['cars'][car_id]
    return web.json_response(local_data)


@aiohttp_jinja2.template('payment_form.html')
async def do_payment(request):
    data = await request.post()
    try:
        card_number = data['card-number']
        year = data['year']
        month = data['month']
        cvv = data['cvv']
        card_holder = data['card-holder']
        try:
            payment_sum = int(data['payment-sum'])
        except Exception as e:
            print(e)
            payment_sum = data['payment-sum']
            return {'error': e}
        if card_number and year and month and cvv and card_holder:
            client = InplatClient()
            pay_params = {
                'pan': card_number,
                'expire_month': month,
                'expire_year': year,
                'cvv': cvv,
                'cardholder_name': card_holder,
            }
            params = {
                'sum': payment_sum,
                'account': data['account'],
            }
            response = client.init(pay_type='card',
                                   client_id=data['user-id'],
                                   pay_params=pay_params,
                                   params=params)
            return {'success': True, 'id': response['id'], 'url': response['id']}
        else:
            return {'user_id': data['user-id'], 'account': data['account'], 'sum': payment_sum,
                    'error': 'Заполните все поля'}
    except InplatException as e:
        raise HTTPInternalServerError(reason=e)


async def do_rest_payment(request):
    data = await request.post()
    try:
        card_number = data['card-number']
        year = data['year']
        month = data['month']
        cvv = data['cvv']
        card_holder = data['card-holder']
        try:
            payment_sum = int(data['payment-sum'])
        except Exception as e:
            payment_sum = data['payment-sum']
            return {'error': e}
        if card_number and year and month and cvv and card_holder:
            client = InplatClient()
            pay_params = {
                'pan': card_number,
                'expire_month': month,
                'expire_year': year,
                'cvv': cvv,
                'cardholder_name': card_holder,
            }
            params = {
                'sum': payment_sum,
                'account': data['account'],
            }
            response = client.init(pay_type='card',
                                   client_id=data['user-id'],
                                   pay_params=pay_params,
                                   params=params)
            return {'success': True, 'id': response['id'], 'url': response['id']}
        else:
            return {'user_id': data['user-id'], 'account': data['account'], 'sum': payment_sum,
                    'error': 'Заполните все поля'}
    except InplatException as e:
        return web.json_response({'error': e.message, 'status': e.code})


@aiohttp_jinja2.template('rest_payment_form.html')
async def rest_payment_form(request):
    user_id = 123123  # Get user id from session
    account = 3423423  # Get account number from system
    payment_sum = 1234  # Get sum from system
    return {'user_id': user_id, 'account': account, 'sum': payment_sum}


@aiohttp_jinja2.template('payment_form.html')
async def payment_form(request):
    user_id = 123123  # Get user id from session
    account = 3423423  # Get account number from system
    payment_sum = 1234  # Get sum from system
    return {'user_id': user_id, 'account': account, 'sum': payment_sum}


class CarsListView(web.View):
    async def get(self):
        return await cars_list(self.request)


class CarsDetailView(web.View):
    async def get(self):
        return await cars_detail(self.request)


class PaymentView(web.View):
    async def get(self):
        return await payment_form(self.request)

    async def post(self):
        return await do_payment(self.request)


class RestPaymentView(web.View):
    async def get(self):
        return await rest_payment_form(self.request)

    async def post(self):
        return await do_rest_payment(self.request)