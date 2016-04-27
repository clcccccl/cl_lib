# -*- coding: utf-8 -*-
#!/usr/bin/env python

import ConfigParser
import pdb


# def listToTree(data_list, parent_key, self_key, ok_list=[]):
#     '''
#     传入data_list和父子关联关系，返回一个树
#     ok_list 存放弄好的树
#     gen_list 存放现在的叶子节点
#     data_list 存放散列的元素
#     '''
#     gen_list = []
#     #将散列的元素中可作为现在树的叶子的元素添加到树上并放到叶子节点中
#     for data1 in data_list:
#         is_child = 0
#         for data2 in data_list:
#             if data1[parent_key] == data2[self_key]:
#                 child_list.append(data1)
#                 is_child = 1
#                 break
#         if is_child == 0:
#             gen_list.append(data1)
#     test_list = []
#     for child in child_list:
#         is_child = 0
#         for gen in gen_list:
#             if child[parent_key] == gen[self_key]:
#                 is_child = 1
#                 gen['child'] = child
#                 child_list
#         if is_child == 0:
#             test_list.append(child)
#     child_list = test_list
#     if len(child_list) == 0:
#         return gen_list
#     else:
#         return listToTree(child_list, parent_key, self_key)


def listToTree(data_list, parent_key, self_key):
    '''
    传入data_list和父子关联关系，返回一个树
    '''
    gen_list = []
    child_list = []
    for data1 in data_list:
        is_child = 0
        for data2 in data_list:
            if data1[parent_key] == data2[self_key]:
                child_list.append(data1)
                is_child = 1
                break
        if is_child == 0:
            gen_list.append(data1)
    for gen in gen_list:
        childs, child_list = findChildInChildList(gen, child_list, parent_key, self_key)
        gen['child'] = childs
    return gen_list


def findChildInChildList(gen, child_list, parent_key, self_key):
    '''
    在child_list中找到gen的所有child
    找到后从child_list中删除这些元素
    返回childs，剩余的child_list
    若找到child，则调用自己找其child
    '''
    childs = []
    test_list = []
    for child in child_list:
        if gen[self_key] == child[parent_key]:
            childs.append(child)
        else:
            test_list.append(child)
    if len(test_list) == 0:
        return childs, child_list
    else:
        gen_list = childs
        for gen in gen_list:
            # print gen
            childs, test_list = findChildInChildList(gen, test_list, parent_key, self_key)
            gen['child'] = childs
            # print gen
        return gen_list, test_list


def getIniConfig(parameter, file_path):
    '''
    传入group和keys({'group': '...', 'keys': ['...',...]})
    检索config.ini,获取值,返回{}
    '''
    re_map = {}
    group = parameter['group']
    keys = parameter['keys']
    config = ConfigParser.ConfigParser()
    with open(file_path, 'r') as config_file:
        config.readfp(config_file)
        for key in keys:
            re_map[key] = config.get(group, key)
    return re_map


def cutStr(value, length):
    '''
    传入需要截取的字符串和长度
    截取长度内的字符串
    '''
    value = value.encode("utf-8")
    if len(value) > length:
        i = 0
        if len(value) > 0:
            while(i < len(value)):
                if ord(value[i]) > 127:
                    if (i + 3) < length:
                        i += 3
                    else:
                        break
                else:
                    if (i + 1) < length:
                        i += 1
                    else:
                        break
        return value[:i]
    else:
        return value


class Storage(dict):

    """
    Storage 就是把 python 的字典的 get set 方法 override 了
    这样用起来比较方便
        >>> o = storage(a=1)
        >>> o.a
        1
        >>> o['a']
        1
        >>> o.a = 2
        >>> o['a']
        2
        >>> del o.a
        >>> o.a
        Traceback (most recent call last):
            ...
        AttributeError: 'a'

    """

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __repr__(self):
        return '<Storage ' + dict.__repr__(self) + '>'


class ClError(Exception):

    def __init__(self, value, error_data):
        print value
        self.value = value
        self.error_data = error_data

    def __str__(self):
        return repr(self.value)


class ClBaseError(Exception):

    def __init__(self, value):
        print value
        self.value = value

    def __str__(self):
        return repr(self.value)

if __name__ == "__main__":
    pass
