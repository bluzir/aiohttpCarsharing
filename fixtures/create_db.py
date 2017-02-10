# -*- coding: utf-8 -*-
from models import *
from utils.utils import generate_uuid


def main():
    db = database
    db.drop_tables(models=[User, Car, Payment, Invoice, Tariff], cascade=True)

    db.create_tables(models=[User, Car, Payment, Invoice, Tariff])

    tariff = Tariff.create(name='Базовый')

    user = User.create(first_name='Vladislav',
                       last_name='Kooklev',
                       email='bluzir@bluzir.me',
                       password='qweqwe',
                       phone_number='1234567',
                       status=1,
                       tariff=tariff)

    payment = Payment.create(status=1)
    Invoice.create(summ=654, user=user, uuid=generate_uuid())
    Invoice.create(summ=1234, user=user, uuid=generate_uuid(), payment=payment)


    Car.create(wialon_id=1,
               car_model='Hyundai Solaris',
               status=1,
               lat=59.9258,
               long=30.2878)

    Car.create(wialon_id=2,
               car_model='Toyota Camry',
               status=1,
               lat=59.9258,
               long=30.2878)

    Car.create(wialon_id=3,
               car_model='Kia Ceed',
               status=2,
               lat=59.9258,
               long=30.2878)


if __name__ == '__main__':
    main()