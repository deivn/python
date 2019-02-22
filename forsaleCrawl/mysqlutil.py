#! /usr/bin/env python  
# -*- coding:utf-8 -*-
import MySQLdb
from scrapy import log
from scrapy.conf import settings
"""
scrapy.log.CRITICAL
严重错误的 Log 级别

scrapy.log.ERROR
错误的 Log 级别 Log level for errors

scrapy.log.WARNING
警告的 Log 级别 Log level for warnings

scrapy.log.INFO
记录信息的 Log 级别(生产部署时推荐的 Log 级别)

scrapy.log.DEBUG
调试信息的 Log 级别(开发时推荐的 Log 级别)
"""


class MysqlHelper(object):

    def __init__(self, charset='utf8'):
        self.host = settings['MYSQL_HOST']
        self.port = settings['MYSQL_PORT']
        self.db = settings['MYSQL_DB']
        self.user = settings['MYSQL_USER']
        self.passwd = ''
        self.charset = charset

    def connect(self):
        self.conn = MySQLdb.connect(host=self.host, port=self.port, db=self.db, user=self.user, passwd=self.passwd, charset=self.charset)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    @staticmethod
    def get_one(sql, params=()):
        result = None
        try:
            MysqlHelper().connect()
            MysqlHelper().cursor.execute(sql, params)
            result = MysqlHelper().cursor.fetchone()
            MysqlHelper().close()
        except Exception as e:
            print(e)
        return result

    @staticmethod
    def get_all(sql, params=()):
        list = ()
        try:
            MysqlHelper().connect()
            MysqlHelper().cursor.execute(sql, params)
            list = MysqlHelper().cursor.fetchall()
            MysqlHelper().close()
        except Exception as e:
            print(e)
        return list

    @staticmethod
    def insert(sql, params=()):
        return MysqlHelper().__edit(sql, params)

    @staticmethod
    def update(sql, params=()):
        return MysqlHelper().__edit(sql, params)

    @staticmethod
    def delete(sql, params=()):
        return MysqlHelper().__edit(sql, params)


    def __edit(self, sql, params):
        count = 0
        try:
            self.connect()
            count = self.cursor.execute(sql, params)
            self.conn.commit()
            self.close()
        except Exception as e:
            print(e)
            # log.msg(e.message, log.ERROR)
        return count
