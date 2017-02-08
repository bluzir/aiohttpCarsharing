from peewee import SelectQuery, Model
from playhouse.shortcuts import model_to_dict

from models import Car, User


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


class CarSerializer(BaseSerializer):
    name = 'cars'
    select_query = SelectQuery(Car, Car.id, Car.car_model)


class UserSerializer(BaseSerializer):
    name = 'users'
    select_query = SelectQuery(User, User.id, User.first_name, User.last_name )

