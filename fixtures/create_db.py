# -*- coding: utf-8 -*-
from models import *


def main():
    db = database

    db.drop_tables(models=[User, Car, Payment, Invoice], cascade=True)

    db.create_table(User)
    db.create_table(Payment)
    db.create_table(Invoice)
    db.create_table(Car)

    user = User.create(first_name='Vladislav',
                       last_name='Kooklev',
                       email='bluzir@bluzir.me',
                       password='qweqwe',
                       phone_number='1234567',
                       status=1)

    Invoice.create(summ=654, user=user)

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