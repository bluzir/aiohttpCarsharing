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
    session = await get_session(request)
    return {'session': session}


# GET '/profile/':
@aiohttp_jinja2.template('profile.html')
async def profile_view(request):
    session = await get_session(request)
    if 'auth_token' in session:
        user_id = User.decode_auth_token(session['auth_token'])
        if user_id:
            return {'token': session['auth_token'], 'session': session}

    return web.HTTPFound('/login/')


# GET '/payments/':
@aiohttp_jinja2.template('payment_list.html')
async def payments_view(request):
    session = await get_session(request)
    if 'auth_token' in session:
        user_id = User.decode_auth_token(session['auth_token'])
        if user_id:
            return {'token': session['auth_token'], 'session': session}

    return web.HTTPFound('/login/')


# GET '/payments/{uuid}':
@aiohttp_jinja2.template('payment_detail.html')
async def payment_detail(request):
    session = await get_session(request)
    payment_uuid = request.match_info['payment_uuid']
    invoice = Invoice.get(uuid=payment_uuid)
    return {'invoice': invoice, 'inplat_api_key': config.INPLAT_API_KEY, 'session': session}


# POST '/payment/{uuid}' :
async def do_payment(request):
    data = await request.post()
    invoice_uuid = request.match_info['payment_uuid']
    try:
        crypto = data['inplat_payment_crypto_input']
        invoice = Invoice.get(uuid=invoice_uuid)
        result = invoice.handle_form(crypto=crypto)
    except KeyError:
        result = {'error': 'No cryptograma'}
    return web.json_response(result)


# GET '/tariff/':
@aiohttp_jinja2.template('tariff.html')
async def tariff_view(request):
    session = await get_session(request)
    if 'auth_token' in session:
        user_id = User.decode_auth_token(session['auth_token'])
        if user_id:
            return {'token': session['auth_token'], 'session': session}

    return web.HTTPFound('/login/')


# GET '/cars/list/' :
async def cars_list(request):
    cars_query = Car.get_available_cars()
    cars_json = CarSerializer(cars_query).get_serialized_json()
    return web.json_response(cars_json)


# GET '/cars/list/{id}' :
async def cars_detail(request):
    try:
        car_id = int(request.match_info['car_id'])
        cars_query = Car.get(id=car_id)
        cars_json = CarSerializer(cars_query).get_serialized_json()
        return web.json_response(cars_json)
    except Car.DoesNotExist:
        return web.HTTPNotFound()
    except Exception:
        return web.HTTPInternalServerError()


# GET '/map/' :
@aiohttp_jinja2.template('maps.html')
async def cars_map(request):
    session = await get_session(request)
    api_key = config.GMAPS_API_KEY
    return {'api_key': api_key, 'session': session}


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


# GET '/login/' :
@aiohttp_jinja2.template('auth_form.html')
async def login(request):
    session = await get_session(request)
    if 'auth_token' in session:
        decoded = User.decode_auth_token(session['auth_token'])
        if decoded:
            return web.HTTPFound('/profile/')
    return {'session': session}


# POST '/login/ :
async def do_login(request):
    data = await request.post()
    session = await get_session(request)
    try:
        email = data['email']
        password = data['password']
        if email and password:
            user = User.get(email=email, password=password)
            auth_token = user.encode_auth_token().decode("utf-8")
            session['auth_token'] = auth_token
            session['is_authorized'] = True
            return web.json_response({'auth_token': auth_token})
        else:
            error = 'Заполните все необходимые поля'
    except User.DoesNotExist:
        error = 'Введены неправильный логин или пароль'
    except KeyError:
        error = 'Заполните все необходимые поля'
    except Exception as e:
        error = e.__traceback__  # TODO: Remove after debug

    return web.json_response({'error': error})


# GET '/logout/' :
async def do_logout(request):
    session = await get_session(request)
    if 'auth_token' in session:
        del session['auth_token']
        del session['is_authorized']
        return web.HTTPFound('/')
    else:
        return web.HTTPFound('/login/')


