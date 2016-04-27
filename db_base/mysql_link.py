#coding:utf-8
from peewee import *
import datetime
import uuid

host = '127.0.0.1'
user = 'root'
passwd = 'root'
database = 'coonever'
charset = 'utf8'
port = 3306


def getDb(host=host, user=user, passwd=passwd, database=database, charset=charset, port=port):
    return MySQLDatabase(host=host, user=user, passwd=passwd, database=database, charset=charset, port=port)


if __name__ == "__main__":
    pass
