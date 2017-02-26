import json

from models.tariff import Tariff
from models.user import User
from models.ride import Ride
from models.car import Car
from models.invoice import Invoice


def main():
    Tariff.create(name='Базовый',
                  description="Бронирование: Бесплатно \nАренда: 8 Р/мин\nОжидание: 2.5 Р/мин")

    with open('fixtures/users.json') as users_file:
        users_json = json.load(users_file)
        users = users_json['users']
        for u in users:
            User.create(**u)

    with open('fixtures/invoices.json') as invoices_file:
        invoices_json = json.load(invoices_file)
        invoices = invoices_json['invoices']
        for i in invoices:
            Invoice.create(**i)

    with open('fixtures/cars.json') as cars_file:
        cars_json = json.load(cars_file)
        cars = cars_json['cars']
        for c in cars:
            Car.create(**c)

    with open('fixtures/rides.json') as rides_file:
        rides_json = json.load(rides_file)
        rides = rides_json['rides']
        for r in rides:
            Ride.create(**r)


if __name__ == '__main__':
    main()