import json

import aiohttp_jinja2 as aiohttp_jinja2
from aiohttp import web

import settings

from models import Payment, Invoice

with open("cars_data.json") as cars_json:
    cars_data = json.loads(cars_json.read())


# GET '/' :
@aiohttp_jinja2.template('index.html')
async def index(request):
    routes = request.app.router._resources
    return {'routes': routes}


# GET '/cars/list/' :
async def cars_list(request):
    return web.json_response(cars_data)


# GET '/cars/list/{id}' :
async def cars_detail(request):
    car_id = int(request.match_info['car_id'])
    local_data = cars_data['cars'][car_id]
    return web.json_response(local_data)


# GET '/map/' :
@aiohttp_jinja2.template('maps.html')
def cars_map(request):
    api_key = settings.GMAPS_API_KEY
    return {'api_key': api_key}


# GET '/payment/' :
@aiohttp_jinja2.template('rest_payment_form.html')
async def payment_form(request):
    user_id = 1  # Get user id from session
    invoice = Invoice.get(id=1)
    return {'user_id': user_id, 'invoice_id': invoice.id, 'invoice_sum': invoice.summ}


# POST '/payment/' :
async def do_payment(request):
    data = await request.post()
    invoice_id = data['invoice_id']
    invoice = Invoice.get(id=invoice_id)
    result = invoice.handle_form(data)
    return web.json_response(result)


# GET '/login/' :
@aiohttp_jinja2.template('auth_form.html')
async def login(request):
    return {}


# POST '/login/ :
async def do_login(request):
    data = await request.post()
    session = await request.session()
    return web.json_response({})




