from peewee import SelectQuery, Model
from playhouse.shortcuts import model_to_dict

from models import Car


class BaseSerializer:
    name = None
    select_query = None

    def __init__(self, query):
        self.query = query
        self.json = None

    def serialize(self):
        if self.query and self.name:
            cars_dict = dict()
            if isinstance(self.query, Model):
                cars_dict[self.name] = model_to_dict(self.query, fields_from_query=self.select_query)
            else:
                cars_dict[self.name] = []
                for item in self.query:
                    serialized = model_to_dict(item, fields_from_query=self.select_query)
                    cars_dict[self.name].append(serialized)
            self.json = cars_dict


class CarSerializer(BaseSerializer):
    name = 'cars'
    select_query = SelectQuery(Car, Car.id, Car.car_model)

