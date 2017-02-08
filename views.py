# -*- coding: utf-8 -*-
import logging

import aiohttp_jinja2 as aiohttp_jinja2
from aiohttp import web

from config import base_settings as config
from models import Invoice, User, Car
from serializers import CarSerializer, UserSerializer, TariffSerializer


# GET '/' :
@aiohttp_jinja2.template('index.html')
async def index(request):
    routes = request.app.router._resources
    return {'routes': routes}


# GET '/cars/list/' :
async def cars_list(request):
    cars_query = Car.get_available_cars()
    serializer = CarSerializer(cars_query)
    serializer.serialize()
    return web.json_response(serializer.json)


# GET '/cars/list/{id}' :
async def cars_detail(request):
    car_id = int(request.match_info['car_id'])
    cars_query = Car.get(id=car_id)
    serializer = CarSerializer(cars_query)
    serializer.serialize()
    return web.json_response(serializer.json)


# GET '/map/' :
@aiohttp_jinja2.template('maps.html')
def cars_map(request):
    api_key = config.GMAPS_API_KEY
    return {'api_key': api_key}


# GET '/api/profile/' :
def profile_detail(request):
    try:
        auth_token = request.GET['auth_token']
        user_id = User.decode_auth_token(auth_token=auth_token)
        if 'error' not in user_id:
            user = User.get(id=user_id['user_id'])
            user_serializer = UserSerializer(user)
            user_serializer.serialize()
            return web.json_response(user_serializer.json)
        else:
            return web.json_response(user_id)
    except KeyError:
        return web.json_response({'error': 'No access token passed'})


# GET '/api/tariff/' :
def tariff_detail(request):
    try:
        auth_token = request.GET['auth_token']
        user_id = User.decode_auth_token(auth_token=auth_token)
        if 'error' not in user_id:
            user = User.get(id=user_id['user_id'])
            tariff = user.tariff
            tariff_serializer = TariffSerializer(tariff)
            tariff_serializer.serialize()
            return web.json_response(tariff_serializer.json)
        else:
            return web.json_response(user_id)
    except KeyError:
        return web.json_response({'error': 'No access token passed'})


# GET '/payment/' :
@aiohttp_jinja2.template('rest_payment_form.html')
async def payment_form(request):
    user_id = 1  # Get user id from session
    invoice = Invoice.get(id=1)
    return {'user_id': user_id, 'invoice_id': invoice.id,
            'invoice_sum': invoice.summ, 'inplat_api_key': config.INPLAT_API_KEY}


# POST '/payment/' :
async def do_payment(request):
    data = await request.post()
    try:
        invoice_id = request.GET['invoice_id']
        crypto = data['inplat_payment_crypto_input']
        invoice = Invoice.get(id=invoice_id)
        result = invoice.handle_form(crypto=crypto)
    except KeyError as e:
        result = {'error': 'No cryptograma'}
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
        user = User.get(email=email, password=password)
        auth_token = user.encode_auth_token().decode("utf-8")
        return web.json_response({'auth_token': auth_token})
    except KeyError:
        return web.json_response({'error': 'Заполните все необходимые поля'})
    except Exception as e:
        return web.json_response({'error': e})


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




