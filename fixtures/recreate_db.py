from models import *

def main():
    if User.table_exists():
        User.drop_table(cascade=True)

    User.create_table()

    if Invoice.table_exists():
        Invoice.drop_table(cascade=True)

    Invoice.create_table()

    if Payment.table_exists():
        Payment.drop_table(cascade=True)

    Payment.create_table()

    if Tariff.table_exists():
        Tariff.drop_table(cascade=True)

    Tariff.create_table()

    if Car.table_exists():
        Car.drop_table(cascade=True)

    Car.create_table()


if __name__ == '__main__':
    main()




