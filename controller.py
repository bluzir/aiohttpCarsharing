# -*- coding: utf-8 -*-

import aiohttp_jinja2 as aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from aiohttp_swagger import swagger_path

import setting as config
from decorator import session_decorator, token_required, check_token, log_request
from error import _error
from model.car import Car
from model.invoice import Invoice
from model.ride import Ride
from model.user import User
from model.payment import Payment
from serializer import CarSerializer, UserSerializer, TariffSerializer, InvoiceSerializer, RideSerializer

from model.payment import PaymentStatus

import logging

from lib.inplat import Inplat


# GET '/' :
@aiohttp_jinja2.template('index.html')
@session_decorator()
async def index(request):
    return {}


# GET '/profile/':
@aiohttp_jinja2.template('profile.html')
@token_required()
async def profile_view(request):
    return {}


# GET '/map/' :
@aiohttp_jinja2.template('maps.html')
@token_required()
async def cars_map(request):
    api_key = config.GMAPS_API_KEY
    return {'api_key': api_key}


# GET '/payments/':
@aiohttp_jinja2.template('payment_list.html')
@token_required()
async def payments_view(request):
    return {}


# GET '/tariff/':
@aiohttp_jinja2.template('tariff.html')
@token_required()
async def tariff_view(request):
    return {}


@aiohttp_jinja2.template('ride.html')
@token_required()
async def ride_view(request):
    return {}


# GET '/payments/{uuid}':
@aiohttp_jinja2.template('payment_detail.html')
@token_required()
async def payment_detail(request):
    payment_uuid = request.match_info['payment_uuid']
    invoice = Invoice.get(uuid=payment_uuid)
    return {'invoice': invoice, 'inplat_api_key': config.INPLAT_API_KEY}


# POST '/payment/{uuid}' :
async def do_payment(request):
    data = await request.post()
    invoice_uuid = request.match_info['payment_uuid']
    if 'crypto' in data:
        crypto = data['inplat_payment_crypto_input']
        invoice = Invoice.get(uuid=invoice_uuid)
        result = invoice.handle_form(crypto=crypto)
    else:
        result = {'error': 'No cryptograma'}

    return web.json_response(result)


# GET '/api/cars/list/' :
async def cars_list(request):
    cars_query = Car.get_available_cars()
    cars_json = CarSerializer(cars_query).get_serialized_json()
    return web.json_response(cars_json)


# GET '/api/cars/list/{id}' :
async def cars_detail(request):
    try:
        car_id = int(request.match_info['car_id'])
        cars_query = Car.get(id=car_id)
        cars_json = CarSerializer(cars_query).get_serialized_json()
        return web.json_response(cars_json)
    except Car.DoesNotExist:
        return web.HTTPNotFound()
    except Exception as e:
        return web.HTTPInternalServerError(text=e.__traceback__)  # TODO: Remove after debug


# GET '/api/profile/' :
@check_token()
@log_request()
@swagger_path("doc/profile.yaml")
def profile_detail(request, user):
    user_json = UserSerializer(user).get_serialized_json()
    return web.json_response(user_json)


# GET '/api/tariff/' :
@check_token()
@log_request()
def tariff_detail(request, user):
    tariff_json = TariffSerializer(user.tariff).get_serialized_json()
    return web.json_response(tariff_json)


# GET '/api/payments/' :
@check_token()
@log_request()
def payments_list(request, user):
    invoices_json = InvoiceSerializer(user.invoices).get_serialized_json()
    return web.json_response(invoices_json)


@check_token()
@log_request()
def current_ride(request, user):
    current_rides = user.rides.where(Ride.status == 1)
    if current_rides.__len__() == 1:
        ride = current_rides.get()
        rides_json = RideSerializer(ride).get_serialized_json()
        return web.json_response(rides_json)
    else:
        return web.json_response({})


# GET '/registration/
@aiohttp_jinja2.template('registration.html')
@session_decorator()
async def registration(request):
    return {}


# POST '/registration/ :
async def do_registration(request):
    data = await request.post()
    response = await User.handle_registration_form(data, request)
    return response


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
    response = await User.handle_authorization_form(data, request)
    return response


# GET '/logout/' :
async def do_logout(request):
    session = await get_session(request)
    if 'auth_token' in session:
        del session['auth_token']
        return web.HTTPFound('/')
    else:
        return web.HTTPFound('/login/')


# GET '/card/':
@aiohttp_jinja2.template('card/list.html')
@token_required()
async def card_view(request):
    return {}


# GET '/card/link/':
@aiohttp_jinja2.template('card/link.html')
@token_required()
async def card_link_view(request):
    return {'inplat_api_key': config.INPLAT_API_KEY}

# POST '/card/link/':
# TODO: пофиксить
async def do_card_link(request):
    data = await request.post()
    if not 'inplat_payment_crypto_input' in data:
        result = {'error': 'No cryptograma'}

    crypto = data['inplat_payment_crypto_input']

    session = await get_session(request)
    user_id = User.decode_auth_token(session['auth_token'])

    _inplat = Inplat()
    #await _inplat.get_links_by_client_id(user_id)
    result = await _inplat.link_card_by_cryptogramma(user_id, crypto)

    if result['error_code'] == 0:
        return web.HTTPFound(result['url'])
    else:
        return _error.error_response(_error, _error.INPLAT_API_ERROR)

    # 'inplat_payment_crypto_input'
    # return web.json_response(result)

async def api_inplat_redirect(request):
    # проверить валидность?
    query = request.rel_url.query
    logging.debug(query)
    order_id = query['orderId']
    inplat_id = query['pid']

    # блокировки!!! (или транзакции)
    payment = Payment.get(inplat_id=inplat_id)
    user = payment.user.get()

    if payment.status == PaymentStatus.WAIT_FOR_REDIRECT:
        payment.order_id = order_id
        payment.status = PaymentStatus.WAIT_FOR_CALLBACK
        # если пеймент был для привязки, то реврешим всё
        if payment.case == 0:
            _inplat = Inplat()
            await _inplat.refresh_links_by_client_id(user)
    else:
        # ТУДУ: передавать сюда сериализованный пеймент
        logging.debug('ACHTUNG!!! api_inplat_redirect: %s %s') % (order_id, inplat_id)

    payment.save()

    url = request.app.router['card'].url()
    return web.HTTPFound(url)


async def api_inplat_callback(request):
    logging.debug(api_inplat_callback.__name__)
    # захардкожено что это привязка
    # использовать транзакции
    query = request.rel_url.query
    logging.debug(query)

    data = await request.post()
    logging.debug(data)





