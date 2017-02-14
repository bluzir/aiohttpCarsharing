from views import *


def setup_routes(app):
    # Basic urls
    app.router.add_get(path='/', handler=index, name='index')
    app.router.add_get(path='/map/', handler=cars_map, name='cars_map')
    app.router.add_get(path='/profile/', handler=profile_view, name='profile')
    app.router.add_get(path='/payments/', handler=payments_view, name='payments')
    app.router.add_get(path='/tariff/', handler=tariff_view, name='tariff')

    # Payment
    app.router.add_get(path='/payments/{payment_uuid}/', handler=payment_detail, name='payment_detail')
    app.router.add_post(path='/payments/{payment_uuid}/', handler=do_payment, name='do_payment')

    # Authentication
    app.router.add_get(path='/login/', handler=login, name='login')
    app.router.add_post(path='/login/', handler=do_login)
    app.router.add_get(path='/logout/', handler=do_logout, name='logout')

    # REST URL's (Require token in GET parameter)
    app.router.add_get(path='/api/profile/', handler=profile_detail, name='api_profile')
    app.router.add_get(path='/api/tariff/', handler=tariff_detail, name='api_tariff')
    app.router.add_get(path='/api/payments/', handler=payments_list, name='api_payments_list')
    app.router.add_get(path='/api/cars/list/', handler=cars_list, name='api_cars_list')
    app.router.add_get(path='/api/cars/list/{car_id}/', handler=cars_detail, name='api_cars_detail')
