from peewee import SelectQuery, Model
from playhouse.shortcuts import model_to_dict

from models import Car, User, Tariff, Invoice


class BaseSerializer:
    name = None
    select_query = None

    def __init__(self, query):
        self.query = query
        self.json = None

    def serialize(self):
        if self.query and self.name:
            items_dict = dict()
            if isinstance(self.query, Model):
                items_dict[self.name] = model_to_dict(self.query, fields_from_query=self.select_query)
            else:
                items_dict[self.name] = []
                for item in self.query:
                    serialized = model_to_dict(item, fields_from_query=self.select_query)
                    items_dict[self.name].append(serialized)
            self.json = items_dict

    def get_serialized_json(self):
        if self.query:
            self.serialize()
            return self.json
        else:
            return False


class CarSerializer(BaseSerializer):
    name = 'cars'
    select_query = SelectQuery(Car, Car.id, Car.car_model, Car.lat, Car.long)


class UserSerializer(BaseSerializer):
    name = 'users'
    select_query = SelectQuery(User, User.id, User.first_name, User.last_name, User.email)


class TariffSerializer(BaseSerializer):
    name = 'tariffs'
    select_query = SelectQuery(Tariff, Tariff.id, Tariff.name)


class InvoiceSerializer(BaseSerializer):
    name = 'invoices'
    select_query = SelectQuery(Invoice, Invoice.id, Invoice.summ, Invoice.payment)