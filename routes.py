from views import cars_list, cars_detail, index, cars_map, payment_form, do_payment


def setup_routes(app):
    # Basic urls
    app.router.add_get(path='/', handler=index, name='index')
    app.router.add_get(path='/map/', handler=cars_map, name='cars_map')

    # Information about cars
    app.router.add_get(path='/cars/list/', handler=cars_list, name='cars_list')
    app.router.add_get(path='/cars/list/{car_id}', handler=cars_detail, name='cars_detail')

    # Payment
    app.router.add_get(path='/payment/', handler=payment_form, name='payment_form')
    app.router.add_post(path='/payment/', handler=do_payment)