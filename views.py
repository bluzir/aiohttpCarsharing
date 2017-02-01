import json

import aiohttp_jinja2 as aiohttp_jinja2
from aiohttp import web
from aiohttp.web_exceptions import HTTPInternalServerError

import settings
from inplat_wrapper.api import InplatException

from models import Payment


# GET '/' :
# Get index page
@aiohttp_jinja2.template('index.html')
async def index(request):
    routes = request.app.router._resources
    return {'routes': routes}


# GET '/cars/list/' :
# Get a list of cars
async def cars_list(request):
    return web.json_response({})


# GET '/cars/list/{id}' :
# Get a specific car by ID
async def cars_detail(request):
    car_id = int(request.match_info['car_id'])
    # local_data = data['cars'][car_id]
    return web.json_response({})


# GET '/map/' :
# Get a Google Map with a cars
@aiohttp_jinja2.template('maps.html')
def cars_map(request):
    api_key = settings.GMAPS_API_KEY
    return {'api_key': api_key}


# GET '/payment/' :
# Get a payment form
@aiohttp_jinja2.template('rest_payment_form.html')
async def payment_form(request):
    user_id = 123123  # Get user id from session
    payment_id = 3423423  # Get account number from system
    payment_sum = 1234  # Get sum from system
    return {'user_id': user_id, 'payment_id': payment_id, 'sum': payment_sum}


# POST '/payment/' :
# Post a payment form
async def do_payment(request):
    data = await request.post()
    payment_id = data['payment_id']
    payment = Payment.get_or_create(id=payment_id)
    payment_result = payment.handle_form(data)
    return web.json_response(payment_result)


@aiohttp_jinja2.template('auth.html')
async def auth_form(request):
    return {}




