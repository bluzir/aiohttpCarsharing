# -*- coding: utf-8 -*-
import json

import aiohttp_jinja2 as aiohttp_jinja2
from aiohttp import web
from playhouse.shortcuts import model_to_dict

import settings

import peewee

from models import Invoice, User, Car


# GET '/' :
from utils.decimal_encoder import DecimalEncoder


@aiohttp_jinja2.template('index.html')
async def index(request):
    routes = request.app.router._resources
    return {'routes': routes}


# GET '/cars/list/' :
async def cars_list(request):
    cars_query = Car.get_available_cars()
    cars_dict = dict()
    cars_dict['cars'] = []
    for item in cars_query:
        serialized = model_to_dict(item)
        cars_dict['cars'].append(serialized)
    return web.json_response(cars_dict)


# GET '/cars/list/{id}' :
async def cars_detail(request):
    car_id = int(request.match_info['car_id'])
    local_data = {}
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
    try:
        email = data['email']
        password = data['password']
        if email and password:
            user = User.get(email=email, password=password)
            auth_token = user.encode_auth_token().decode("utf-8")
            return web.json_response({'auth_token': auth_token})
        else:
            error = 'Заполните все необходимые полня'
    except KeyError:
        error = 'Заполните все необходимые полня'
    except User.DoesNotExist:
        error = 'Неправильный логин или пароль'
    except Exception as e:
        error = str(e)

    return web.json_response({'error': error})


# GET '/decode_token/'
@aiohttp_jinja2.template('decode_token.html')
async def decode_form(request):
    return {}


# POST '/decode_token/
async def decode_token(request):
    data = await request.post()
    try:
        auth_token = data['token']
        decoded = User.decode_auth_token(auth_token)
        if 'error' not in decoded:
            return web.json_response({'user_id': decoded['user_id']})
        else:
            error = decoded['error']
    except Exception as e:
        error = str(e)
    return web.json_response({'error': error})




