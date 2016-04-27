# -*- coding: utf-8 -*-
#!/usr/bin/env python

'''
管理异常、错误日志、重要信息存入数据库
异常系统异常和自定义异常
'''


class ClException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

if __name__ == "__main__":
    pass
