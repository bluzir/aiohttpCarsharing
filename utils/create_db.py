from models import *


def main():
    db = database
    db.create_table(User)
    db.create_table(Car)
    db.create_table(Payment)
    db.create_table(Invoice)

    user = User.create(first_name='Vladislav',
                       last_name='Kooklev',
                       email='bluzir@bluzir.me',
                       password='qweqwe',
                       phone_number='1234567',
                       status=1)

    Invoice.create(summ=654, user=user)

if __name__ == '__main__':
    main()