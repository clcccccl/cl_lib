# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
import datetime
import time
from base import db_base
import types
import pdb
import uuid

db = db_base.getDb()


def select(table_name, columns='*', where='1=1', limit='0,10'):
    '''
    传入表名,要搜索的列(默认为*),查询条件,分页
    返回一个list,其中元素为map:[{}]
    '''
    sql = '''
        select %s from %s where %s limit %s
    ''' % (columns, table_name, where, limit)
    print sql
    data_list = []
    result = db.execute_sql(sql)
    for array in result:
        data_map = {}
        j = 0
        for value in array:
            data_map[result.description[j][0]] = value
            j += 1
        data_list.append(data_map)
    return data_list


def selectSql(sql="select * from base"):
    '''
    '''
    print sql
    data_list = []
    result = db.execute_sql(sql)
    for array in result:
        data_map = {}
        j = 0
        for value in array:
            data_map[result.description[j][0]] = value
            j += 1
        data_list.append(data_map)
    return data_list


def insert(table_name, values_list):
    '''
    传入表名,要插入的数据[{}]
    因为数据表使用class创建,继承了基础表,在添加数据时加入基础表默认值
    '''
    columns = 'uuid,create_date,modify_date,status,'
    keys = values_list[0].keys()
    for key in keys:
        columns = columns + key + ','
    columns = '(' + columns[0:-1] + ')'
    values = ''
    for value_map in values_list:
        data_uuid = uuid.uuid3(uuid.NAMESPACE_DNS, 'coonever')
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        value = "'" + str(data_uuid) + "','" + time_str + "','" + time_str + "',0"
        for value_one in value_map.values():
            if type(value_one) == long or type(value_one) == int:
                value = value + ',' + repr(value_one)
            elif type(value_one) == unicode:
                value = value + ",'" + value_one.encode('utf-8') + "'"
            elif type(value_one) == str:
                value = value + ",'" + value_one + "'"
        values = values + '(' + value + ')' + ','
    values = values[0:-1]
    sql = '''
        insert into %s %s values %s ;
    ''' % (table_name, columns, values)
    print sql
    db.execute_sql(sql)


def insertOne(table_name, value_map):
    columns = 'uuid,create_date,modify_date,status,'
    keys = value_map.keys()
    for key in keys:
        columns = columns + key + ','
    columns = '(' + columns[0:-1] + ')'
    data_uuid = uuid.uuid3(uuid.NAMESPACE_DNS, 'coonever')
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    value = "'" + str(data_uuid) + "','" + time_str + "','" + time_str + "',0"
    for value_one in value_map.values():
        if type(value_one) == long or type(value_one) == int:
            value = value + ',' + repr(value_one)
        elif type(value_one) == unicode:
            value = value + ",'" + value_one.encode('utf-8') + "'"
        elif type(value_one) == str:
            value = value + ",'" + value_one + "'"
    value = '(' + value + ')'
    sql = '''
        insert into %s %s values %s ;
    ''' % (table_name, columns, value)
    print sql
    db.execute_sql(sql)
    return str(data_uuid)


def update(table_name, value_map, where='1=1'):
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    set_value = "modify_date = '" + time_str + "',"
    keys = value_map.keys()
    values = value_map.values()
    for key in keys:
        if type(value_map[key]) == long or type(value_map[key]) == int:
            set_value = set_value + key + "=" + repr(value_map[key]) + ","
        elif type(value_map[key]) == unicode:
            set_value = set_value + key + "='" + value_map[key].encode('utf-8') + "',"
        elif type(value_map[key]) == str:
            set_value = set_value + key + "='" + value_map[key] + "',"
    set_value = set_value[:-1]
    sql = '''
        update %s set %s where %s ;
    ''' % (table_name, set_value, where)
    print sql
    db.execute_sql(sql)


def delete(table_name, where='1=1'):
    sql = '''
        update %s set status = 1 where %s ;
    ''' % (table_name, where)
    db.execute_sql(sql)


def deleteRel(table_name, where='1=1'):
    sql = '''
        delete %s where %s ;
    ''' % (table_name, where)
    db.execute_sql(sql)

if __name__ == "__main__":
    pass
