from views import index, maps, cars_list, cars_detail


def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_get('/maps', maps)
    app.router.add_get('/cars/list/', cars_list)
    app.router.add_get('/cars/list/{car_id}', cars_detail)