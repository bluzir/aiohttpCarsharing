from views import *


def setup_routes(app):
    # Basic urls
    app.router.add_get(path='/', handler=index, name='index')
    app.router.add_get(path='/map/', handler=cars_map, name='cars_map')
    app.router.add_get(path='/profile/', handler=profile_view, name='profile')
    app.router.add_get(path='/payments/', handler=payments_view, name='payments')
    app.router.add_get(path='/tariff/', handler=tariff_view, name='tariff')

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
    app.router.add_get(path='/api/payments/', handler=payments_list, name='api_payments_list')
    app.router.add_get(path='/api/cars/list/', handler=cars_list, name='api_cars_list')
    app.router.add_get(path='/api/cars/list/{car_id}', handler=cars_detail, name='api_cars_detail')
