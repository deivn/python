#! /usr/bin/env python  
# -*- coding:utf-8 -*-
import re
import math
import time
from forsaleCrawl.sqlutil import SqlUtil


class HouseImportOpt(object):
    # 用户ID起始index
    uid = 100
    # 房源类型起始index
    house_type_id = 100

    def __init__(self):
        pass

    @staticmethod
    def get_sql_info_by_code(item, tab_name, code):
        """
        功能：根据表名，字段列表，生成sql语句
        :param tab_name: 表名
        :param item: 网页爬取的信息
        :return:
        """
        _fields = HouseImportOpt().get_fields_by_code(code)
        sql = SqlUtil.gen_sql_sql(tab_name, _fields)
        params = HouseImportOpt().get_params_by_user_item(item, code)
        return (sql, params)

    def house_type_belongs(self, type_name):
        """
        功能：爬虫爬到的房源类型在现在的数据库房源列表匹配，匹配成功True失败False
        :param type_name:
        :return:
        """
        list = ['Studio', 'House', 'Single family', 'Town house', 'Condos/co-ops', 'Multiple', 'Apartments', 'HighRise', 'Lots/Land', 'All']
        # 先将空格去掉再转小写
        for type in list:
            if type_name == re.sub("\s", "", type).lower():
                return True
        else:
            return False

    def get_fields_by_code(self, code):
        """
        功能：根据code生成对应表的字段列表
        :param code: 字段标识code =1（用户表） 2 房源类型表
        :return:
        """
        _fields = []
        if code == 1:
            _fields = [
                'id', 'phone', 'email', 'password', 'nickname', 'firstname', 'middlename',
                'lastname', 'sex', 'orgin', 'head_url', 'status', 'type', 'email_status',
                'state_id', 'city_id', 'address', 'zip', 'hxusername', 'phone_area_code_id',
                'create_time'
            ]
        elif code == 2:
            _fields = ['id', 'name', 'is_enable', 'img_url', 'add_time']

        return _fields

    def get_params_by_user_item(self, item, code):
        """
        功能：根据用户item生成数据库表的参数列表
        :param item:
        :param current_time:
        :param code:1用户表参数 2房源类型表参数
        :return:
        """
        params = []
        if code == 1:
            # 当前时间 yyyy-MM-dd HH:mm:ss
            current_time = SqlUtil.gen_current_time()
            self.uid += 1
            params = [self.uid, item['phone'], ' ', ' ', ' ', ' ', ' ', ' ',
                      3, 1, ' ', 1, 1, 1, item['addressRegion'], item['cityId'],
                      item['streetAddress'], item['postalCode'], ' ', ' ', current_time]
        elif code == 2:
            house_type = item['structure_type'].replace(" ", "").lower()
            if_belongs = self.house_type_belongs(house_type)
            # 数据库没有
            if not if_belongs:
                # 取图片列表第一张
                self.house_type_id += 1
                img_url = item['pics'][0] if len(item['pics']) else ''
                add_time = math.floor(time.time())
                params = [self.house_type_id, house_type, 1, img_url, add_time]
        return params