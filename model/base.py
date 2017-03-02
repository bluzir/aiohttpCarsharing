from peewee import Model
from peewee_asyncext import PostgresqlExtDatabase

import base_settings as config

# database = PostgresqlDatabase(config.DB_NAME, user=config.DB_USER, password=config.DB_PASSWORD, host=config.DB_HOST)
database = PostgresqlExtDatabase(config.DB_NAME, user=config.DB_USER,
                                 password=config.DB_PASSWORD, host=config.DB_HOST, register_hstore=False)


class BaseModel(Model):
    class Meta:
        database = database