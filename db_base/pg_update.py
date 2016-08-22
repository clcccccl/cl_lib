# -*- coding: utf-8 -*-
#!/usr/bin/env python

'''
数据库的增删改接口
'''

import time
import pg_base
import pdb
import datetime


def select(table_name, columns='*', where='', limit=10, offset=0, order_by="create_date desc"):
    '''
    传入表名,要搜索的列(默认为*),查询条件,分页
    返回一个list,其中元素为map:[{}]
    '''
    limit_str = '' if limit == -1 else ' limit %s ' % limit
    where = ' status = 0 ' if where == '' else (where + ' and status = 0 ')
    sql = '''
        select %s from %s where %s order by %s %s offset %d
    ''' % (columns, table_name, where, order_by, limit_str, offset)
    return selectBySql(sql)


def selectBySql(sql):
    '''
    传入sql
    返回一个list,其中元素为map:[{}]
    '''
    datas = pg_base.pg_db.query(sql)
    keys = []
    for data in datas:
        for key in data.keys():
            if isinstance(data[key], datetime.datetime):
                keys.append(key)
        break
    for key in keys:
        for data in datas:
            data[key] = str(data[key])
    return datas


def insert(table_name, values_list):
    '''
    传入表名,要插入的数据[{}]
    因为数据表使用class创建,继承了基础表,在添加数据时加入基础表默认值
    '''
    if len(values_list) == 0:
        return
    columns = 'create_date,modify_date,status,' + ','.join(values_list[0].keys())
    values = ''
    for value_map in values_list:
        value = " now(), now() ,0"
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
        insert into %s (%s) values %s ;
    ''' % (table_name, columns, values)
    pg_base.pg_db.modifyData(sql)


def insertOne(table_name, value_map, return_id=False):
    if return_id:
        value_map['id'] = getSeq(table_name)
    columns = 'create_date,modify_date,status,' + ','.join(value_map.keys())
    value = " now(), now() ,0"
    for value_one in value_map.values():
        if type(value_one) == long or type(value_one) == int:
            value = value + ',' + repr(value_one)
        elif type(value_one) == unicode:
            value = value + ",'" + value_one.encode('utf-8') + "'"
        elif type(value_one) == str:
            value = value + ",'" + value_one + "'"
    sql = '''
        insert into %s (%s) values (%s) ;
    ''' % (table_name, columns, value)
    pg_base.pg_db.modifyData(sql)
    return value_map['id'] if return_id else None


def update(table_name, value_map, where='1=1'):
    if value_map.get('modify_date'):
        del value_map['modify_date']
    if value_map.get('create_date'):
        del value_map['create_date']
    set_value = ''
    for key in value_map.keys():
        if type(value_map[key]) == long or type(value_map[key]) == int:
            set_value = set_value + key + "=" + repr(value_map[key]) + ","
        elif type(value_map[key]) == unicode:
            set_value = set_value + key + "='" + value_map[key].encode('utf-8') + "',"
        elif type(value_map[key]) == str:
            set_value = set_value + key + "='" + value_map[key] + "',"
    set_value = "modify_date = now(), " + set_value[:-1] if set_value else "modify_date = now()"
    sql = '''
        update %s set %s where %s ;
    ''' % (table_name, set_value, where)
    pg_base.pg_db.modifyData(sql)


def softDelete(table_name, where='1=1'):
    sql = '''
        update %s set modify_date = now(),status = 1 where %s ;
    ''' % (table_name, where)
    pg_base.pg_db.modifyData(sql)


def delete(table_name, where='1=1'):
    sql = '''
        delete from %s where %s ;
    ''' % (table_name, where)
    pg_base.pg_db.modifyData(sql)


def relDelete(table_name, where='1=1'):
    sql = '''
        delete from %s where %s ;
    ''' % (table_name, where)
    pg_base.pg_db.modifyData(sql)


def getSeq(table_name):
    sql = '''
        select nextval('%s_id_seq') as new_id
    ''' % table_name
    return int(pg_base.pg_db.query(sql)[0]['new_id'])


def reCreateTable(the_model):
    '''
    重建表
    '''
    if the_model.table_exists():
        the_model.drop_table()
        createTable(the_model)
    else:
        print "数据表不存在"


def createTable(the_model):
    '''
    新建表
    '''
    if the_model.table_exists():
        print "数据表已经存在了"
    else:
        the_model.create_table()


def forciblyCreateTable(the_model):
    '''
    强制新建表
    '''
    if the_model.table_exists():
        print "数据表已经存在了"
        the_model.drop_table()
        createTable(the_model)
    else:
        the_model.create_table()


def dropTable(the_model):
    '''
    新建表
    '''
    if the_model.table_exists():
        the_model.drop_table()
    else:
        print "数据表不存在"

if __name__ == "__main__":
    relDelete('user_info')
    insertOne('user_info', {'name': "穿件", 'account': '234', 'password': 'ly'})
    pass
