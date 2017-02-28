from peewee import PostgresqlDatabase, Model

import base_settings as config

database = PostgresqlDatabase(config.DB_NAME, user=config.DB_USER, password=config.DB_PASSWORD, host=config.DB_HOST)


class BaseModel(Model):
    class Meta:
        database = database