# -*- coding: utf-8 -*-
#!/usr/bin/env python

import psycopg2
import sys
import os
import pdb
import datetime
from playhouse.postgres_ext import PostgresqlExtDatabase
from peewee import *
import traceback

import tools

reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.UTF8'

pg_db = None
db = None


class PgDB:
    '''
    postgrasql数据操作
    '''
    def __init__(self, pd_map):
        self.host = pd_map['host']
        self.port = pd_map['port']
        self.db_name = pd_map['db_name']
        self.user = pd_map['user']
        self.password = pd_map['password']
        self.conn = psycopg2.connect(host=self.host, port=self.port,
                                     database=self.db_name, user=self.user, password=self.password)
        print '连接到数据库:' + self.host

    def query(self, sql):
        try:
            out = []
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            names = [x[0] for x in self.cursor.description]
            out = [tools.Storage(dict(zip(names, x))) for x in self.cursor.fetchall()]
            self.cursor.close()
            return out
        except Exception, e:
            print e
            raise
        finally:
            self.cursor.close()

    def get_db(self):
        self.db = PostgresqlExtDatabase(self.db_name, user=self.user, password=self.password, host=self.host, register_hstore=False)
        return self.db

    def modifyData(self, sql):
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            self.conn.commit()
            self.cursor.close()
        except IntegrityError, e:
            self.conn.rollback()
            print e
            raise IntegrityError(e)
        except Exception, e:
            print e
            print sql
            self.conn.rollback()
            raise Exception(e)
        finally:
            self.cursor.close()

    def __exit__(self, exctype, excvalue, traceback):
        self.conn.close()
        print '---断开数据库连接'


def connect():
    global pg_db
    global db
    pg_db = PgDB(tools.getIniConfig({'group': 'pg_db', 'keys': ['port', 'host', 'db_name', 'user', 'password']}, './config.ini'))
    db = pg_db.get_db()


connect()


class BaseTable(Model):
    class Meta:
        database = db
    create_date = DateTimeField(default=datetime.datetime.now)
    modify_date = DateTimeField(default=datetime.datetime.now)
    status = IntegerField(default=0)


class Log(Model):
    '''
        日志表
    '''
    class Meta:
        database = db
    time = DateTimeField(default=datetime.datetime.now)  # 插入时间
    log_type = CharField(max_length=30)  # 日志类型
    log = TextField(null=True)  # 日志
    log_detail = TextField(null=True)  # 日志详细
    business_code = TextField(null=True)  # 日志详细
    user_id = IntegerField(null=True)  # 用户id
    key1 = TextField(null=True)  # 健1
    value1 = TextField(null=True)  # 值1
    key2 = TextField(null=True)  # 健2
    value2 = TextField(null=True)  # 值2
    status = IntegerField(default=0)

if __name__ == '__main__':
    pass
