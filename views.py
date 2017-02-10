# -*- coding: utf-8 -*-
import logging

import aiohttp_jinja2 as aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session

from config import base_settings as config
from models import Invoice, User, Car
from serializers import CarSerializer, UserSerializer, TariffSerializer, InvoiceSerializer


# GET '/' :
@aiohttp_jinja2.template('index.html')
async def index(request):
    routes = request.app.router._resources
    return {'routes': routes}


# GET '/':
@aiohttp_jinja2.template('profile.html')
async def profile_view(request):
    session = await get_session(request)
    if 'auth_token' in session:
        user_id = User.decode_auth_token(session['auth_token'])
        if user_id:
            return {'token': session['auth_token']}

    return web.HTTPFound('/login/')


# GET '/':
@aiohttp_jinja2.template('payments.html')
async def payments_view(request):
    session = await get_session(request)
    if 'auth_token' in session:
        user_id = User.decode_auth_token(session['auth_token'])
        if user_id:
            return {'token': session['auth_token']}

    return web.HTTPFound('/login/')


# GET '/':
@aiohttp_jinja2.template('tariff.html')
async def tariff_view(request):
    session = await get_session(request)
    if 'auth_token' in session:
        user_id = User.decode_auth_token(session['auth_token'])
        if user_id:
            return {'token': session['auth_token']}

    return web.HTTPFound('/login/')


# GET '/cars/list/' :
async def cars_list(request):
    cars_query = Car.get_available_cars()
    cars_json = CarSerializer(cars_query).get_serialized_json()
    return web.json_response(cars_json)


# GET '/cars/list/{id}' :
async def cars_detail(request):
    car_id = int(request.match_info['car_id'])
    cars_query = Car.get(id=car_id)
    cars_json = CarSerializer(cars_query).get_serialized_json()
    return web.json_response(cars_json)


# GET '/map/' :
@aiohttp_jinja2.template('maps.html')
def cars_map(request):
    api_key = config.GMAPS_API_KEY
    return {'api_key': api_key}


# GET '/api/profile/' :
def profile_detail(request):
    if 'token' in request.GET:
        user = User.get_user_by_token(request.GET['token'])
        if user:
            user_json = UserSerializer(user).get_serialized_json()
            return web.json_response(user_json)
        else:
            return web.json_response({'error': 'invalid token'})
    return web.json_response({'error': 'no access token passed'})


# GET '/api/tariff/' :
def tariff_detail(request):
    if 'token' in request.GET:
        user = User.get_user_by_token(request.GET['token'])
        if user:
            tariff_json = TariffSerializer(user.tariff).get_serialized_json()
            return web.json_response(tariff_json)
        else:
            return web.json_response({'error': 'invalid token'})
    return web.json_response({'error': 'no access token passed'})


# GET '/api/payments/' :
def payments_list(request):
    if 'token' in request.GET:
        print(request.GET['token'])
        user = User.get_user_by_token(request.GET['token'])
        if user:
            invoices = user.invoices
            invoices_json = InvoiceSerializer(invoices).get_serialized_json()
            return web.json_response(invoices_json)
        else:
            return web.json_response({'error': 'invalid token'})
    return web.json_response({'error': 'no access token passed'})


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
    session = await get_session(request)
    try:
        email = data['email']
        password = data['password']
        user = User.get(email=email, password=password)
        auth_token = user.encode_auth_token().decode("utf-8")
        session['auth_token'] = auth_token
        session['is_authorized'] = True
        return web.HTTPFound('/profile/')
    except KeyError:
        return web.json_response({'error': 'Заполните все необходимые поля'})
    except Exception as e:
        return web.json_response({'error': e})


# GET '/logout/' :
async def do_logout(request):
    session = await get_session(request)
    if 'auth_token' in session:
        session['auth_token'] = None
        session['is_authorized'] = None
        return web.HTTPFound('/')
    else:
        return web.HTTPFound('/login/')


