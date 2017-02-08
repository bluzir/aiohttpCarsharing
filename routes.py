from views import cars_list, cars_detail, index, cars_map, payment_form, do_payment, login, do_login, decode_form, \
    decode_token, profile_detail, tariff_detail


def setup_routes(app):
    # Basic urls
    app.router.add_get(path='/', handler=index, name='index')
    app.router.add_get(path='/map/', handler=cars_map, name='cars_map')

    # Payment
    app.router.add_get(path='/payment/', handler=payment_form, name='payment_form')
    app.router.add_post(path='/payment/', handler=do_payment)

    # Authentication
    app.router.add_get(path='/login/', handler=login, name='login')
    app.router.add_post(path='/login/', handler=do_login)
    app.router.add_get(path='/decode_token/', handler=decode_form, name='decode')
    app.router.add_post(path='/decode_token/', handler=decode_token)

    # REST URL's
    app.router.add_get(path='/api/profile/', handler=profile_detail, name='api_profile')
    app.router.add_get(path='/api/tariff/', handler=tariff_detail, name='api_tariff')
    app.router.add_get(path='/api/cars/list/', handler=cars_list, name='cars_list')
    app.router.add_get(path='/api/cars/list/{car_id}', handler=cars_detail, name='cars_detail')
