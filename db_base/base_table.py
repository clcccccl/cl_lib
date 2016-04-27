#coding:utf-8
from peewee import *
import datetime
import uuid


class BaseTable(Model):
    class Meta:
        database = db
    uuid = CharField(max_length=40, default=uuid.uuid3(uuid.NAMESPACE_DNS, 'coonever'))
    create_date = DateTimeField(default=datetime.datetime.now)
    modify_date = DateTimeField(default=datetime.datetime.now)
    status = IntegerField(default=0)

if __name__ == "__main__":
    pass
