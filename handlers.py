import logging

import tornado.websocket
from pyrestful import mediatypes
from pyrestful.rest import RestHandler, get

from models import Users


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class RegistrationHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("registration.html", just_registered=False, alert=None)

    async def post(self):
        email = self.get_argument('email', None)
        password = self.get_argument('password', None)

        if email is None or password is None:
            self.render('registration.html', alert='Email and password must not be blank.')
            return


        try:
            await self.application.objects.create(User,
                                                  email=email,
                                                  password=password)

            self.render('registration.html', alert='Successfully registered')
        except Exception as e:
             return self.render('registration.html', alert=str(e))


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html", just_registered=False, alert=None)

    async def post(self):
        email = self.get_argument('email', None)
        password = self.get_argument('password', None)

        if email is None or password is None:
            self.render('registration.html', alert='Email and password must not be blank.')
            return


        try:
            await self.application.objects.create(User,
                                                  email=email,
                                                  password=password)

            self.render('registration.html', alert='Successfully registered')
        except Exception as e:
             return self.render('registration.html', alert=str(e))



class GetUserByIDHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("GET",)

    @tornado.web.authenticated
    async def get(self, id):
        try:
            user = await self.application.objects.get(Users, id=id)
            response = {
                'id': user.id,
                'email': user.email
            }
        except Exception as e:
            response = '{}'.format(e)

        self.write(response)
