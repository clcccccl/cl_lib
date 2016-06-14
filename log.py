#!/usr/bin/env python
#encoding=utf-8
import sys
import logging
log_file = sys.argv[0]
log_file = log_file.replace('.py', '') + '.log'


def initlog(log_file_name=log_file):
    '''初始化一个common.logger对象'''
    logger = logging.getLogger()
    hdlr = logging.FileHandler(log_file_name)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.NOTSET)
    return logger

log_hander = initlog()

if __name__ == '__main__':
    pass
