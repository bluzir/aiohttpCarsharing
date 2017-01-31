from views import index, maps, cars_detail,\
    CarsListView, PaymentView, RestPaymentView


def setup_routes(app):
    # Basic urls
    app.router.add_get('/', index)
    app.router.add_get('/maps', maps)

    # Information about cars
    app.router.add_route('*', '/cars/list/', CarsListView)
    app.router.add_get('/cars/list/{car_id}', cars_detail)

    # Payment
    app.router.add_route('*', '/payment/', PaymentView)
    app.router.add_route('*', '/rest/payment/', RestPaymentView)