from handlers import MainHandler, RegistrationHandler, GetUserByIDHandler


url_patterns = [
    (r"/", MainHandler),
    (r"/registration", RegistrationHandler),
    (r"/user/([0-9]+)", GetUserByIDHandler),
]