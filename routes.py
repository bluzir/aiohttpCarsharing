from views import index, maps, cars_detail, \
    ride_start, ride_end, reservation_start, reservation_end, CarsListView, PaymentView


def setup_routes(app):
    # Basic urls
    app.router.add_get('/', index)
    app.router.add_get('/maps', maps)

    # Information about cars
    app.router.add_route('*', '/cars/list/', CarsListView)
    app.router.add_get('/cars/list/{car_id}', cars_detail)

    # Ride actions
    app.router.add_get('/ride/start/{car_id}', ride_start)
    app.router.add_get('/ride/end/{car_id}', ride_end)

    # Reservation actions
    app.router.add_get('/reservation/start/', reservation_start)
    app.router.add_get('/reservation/end/', reservation_end)

    # Payment
    app.router.add_route('*', '/payment/', PaymentView)