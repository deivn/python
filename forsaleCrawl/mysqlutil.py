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
        self.passwd = settings['MYSQL_PASSWD']
        self.charset = charset

    def connect(self):
        self.conn = MySQLdb.connect(host=self.host, port=self.port, db=self.db, user=self.user, passwd=self.passwd, charset=self.charset)
        self.cursor = self.conn.cursor()

    @staticmethod
    def close():
        MysqlHelper.cursor.close()
        MysqlHelper.conn.close()

    @staticmethod
    def get_one(sql, params=()):
        return MysqlHelper()._find_one(sql, params)

    @staticmethod
    def get_all(sql, param=()):
        return MysqlHelper()._find_all(sql, param)

    def _find_all(self, sql, param):
        list = ()
        try:
            self.connect()
            self.cursor.execute(sql, param)
            list = self.cursor.fetchall()
            # self.close()
        except Exception as e:
            print(e)
        return list

    def _find_one(self, sql, param):
        result = None
        try:
            self.connect()
            self.cursor.execute(sql, param)
            result = self.cursor.fetchone()
            MysqlHelper().close()
        except Exception as e:
            print(e)
        return result

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
            # self.close()
        except Exception as e:
            print(e)
            # log.msg(e.message, log.ERROR)
        return count
