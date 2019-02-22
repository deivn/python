# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import os
from datetime import datetime
from scrapy.conf import settings
from forsaleCrawl.mysqlutil import MysqlHelper
from forsaleCrawl.dealopt import HouseImportOpt


class ForsalecrawlPipeline(object):

    def __init__(self):
        dir = settings['DATA_PATH_PREFIX']
        # 是否存在该目录
        is_exists = os.path.exists(dir)
        if not is_exists:
            os.makedirs(dir)
        today = datetime.now()
        full_path = dir + '/{}{}{}{}{}{}' + '.json'
        data_path = full_path.format(today.year, today.month, today.day, today.hour, today.minute, today.second)
        self.filename = codecs.open(data_path, "w", encoding="utf-8")

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.filename.write(content)
        # 用户信息
        # sql, params = HouseImportOpt.get_sql_info_by_code(item, "t_user", 1)
        # 插入用户表
        # count = MysqlHelper.insert(sql, params)
        # 插入房源类型表
        # sql, params = HouseImportOpt.get_sql_info_by_code(item, "t_house_type", 2)
        # 查询数据据
        # count = MysqlHelper.get_one(sql, params) if params else None
        return item

    def close_spider(self, spider):
        self.filename.close()
        os.close()


