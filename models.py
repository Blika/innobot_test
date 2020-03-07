import peewee

import config


class BaseModel(peewee.Model):
    class Meta:
        database = config.DB


class User(BaseModel):
    tg_id = peewee.BigIntegerField()
    full_name = peewee.CharField()


class Message(BaseModel):
    message_id = peewee.BigIntegerField()
    chat_id = peewee.BigIntegerField()
    text = peewee.TextField()
    user = peewee.ForeignKeyField(User, backref='messages')
