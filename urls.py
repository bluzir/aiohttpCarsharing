from handlers import MainHandler, RegistrationHandler, GetUserByIDHandler, LoginHandler

url_patterns = [
    (r"/", MainHandler),
    (r"/registration", RegistrationHandler),
    (r"/login", LoginHandler),
    (r"/api/user/([0-9]+)", GetUserByIDHandler),
]