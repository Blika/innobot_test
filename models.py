import peewee

import config


class BaseModel(peewee.Model):
    class Meta:
        database = config.DB


class Book(BaseModel):
    name = peewee.TextField()
