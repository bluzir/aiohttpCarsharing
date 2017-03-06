from model.request import Request
from model.payment import Payment
from model.tariff import Tariff
from model.car import Car
from model.user import User
from model.problem import Problem
from model.invoice import Invoice
from model.ride import Ride


def main():
    if Tariff.table_exists():
        Tariff.drop_table(cascade=True)

    Tariff.create_table()

    if Car.table_exists():
        Car.drop_table(cascade=True)

    Car.create_table()

    if Problem.table_exists():
        Problem.drop_table(cascade=True)

    Problem.create_table()

    if User.table_exists():
        User.drop_table(cascade=True)

    User.create_table()

    if Payment.table_exists():
        Payment.drop_table(cascade=True)

    Payment.create_table()

    if Invoice.table_exists():
        Invoice.drop_table(cascade=True)

    Invoice.create_table()

    if Ride.table_exists():
        Ride.drop_table(cascade=True)

    Ride.create_table()

    if Request.table_exists():
        Request.drop_table(cascade=True)

    Request.create_table()


if __name__ == '__main__':
    main()




