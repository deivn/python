# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import os
import re
from datetime import datetime
from scrapy.conf import settings
from forsaleCrawl.mysqlutil import MysqlHelper
from forsaleCrawl.dealopt import HouseImportOpt


class ForsalecrawlPipeline(object):

    def __init__(self):
        # 用户ID起始index
        self.uid = 10000
        # 房源类型起始index
        self.house_type_id = 10000
        # 房源起始index
        self.house_id = 10000
        # 房源辅图表ID起始
        self.house_img_id = 10000

        # 只加载一次 house_type表中的数据
        self.house_types = MysqlHelper.get_all("select name from t_house_type", [])
        # 存储house_type表中的name
        self._names = []
        for name in self.house_types:
            self._names.append(name[0])
    #     dir = settings['DATA_PATH_PREFIX']
    #     # 是否存在该目录
    #     is_exists = os.path.exists(dir)
    #     if not is_exists:
    #         os.makedirs(dir)
    #     today = datetime.now()
    #     full_path = dir + '/{}{}{}{}{}{}' + '.json'
    #     data_path = full_path.format(today.year, today.month, today.day, today.hour, today.minute, today.second)
    #     self.filename = codecs.open(data_path, "w", encoding="utf-8")

    def house_type_belongs(self, type_name):
        """
        功能：爬虫爬到的房源类型在现在的数据库房源列表匹配，匹配成功True失败False
        :param type_name:
        :return:
        """
        return self.flag_contains(type_name)

    def flag_contains(self, type_name):
        """
        判断字段在数据表中是否存在
        :param type_name: 传入的字段
        :return:
        """
        house_type = type_name.replace(" ", "").lower()
        for type in self._names:
            if house_type == re.sub("\s", "", type).lower():
                return True
        else:
            self._names.append(type_name)
            return False

    def process_item(self, item, spider):
        # content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        # self.filename.write(content)
        # 城市信息,根据t_city中的city_ascii和state_id查询
        sql = "select id from t_city where city_ascii = %s and state_id = %s"
        # 根据州ID和城市地址查询
        id = MysqlHelper.get_one(sql, [item['addressLocality'], item['addressRegion']])
        # 如果ID不存在，则不插入房源表， 用户表，房源类型表
        pics = item['pics']
        streetAddress = item['streetAddress']
        lot_size = item['lot_size']
        structure_type = item['structure_type']
        data_flag = False
        if structure_type and streetAddress != '.' and lot_size != 'N/A':
            structure_type = HouseImportOpt.get_column_field(structure_type)
            if id and len(pics):
                # 农场的情况
                if structure_type == 'Lots/Land':
                    data_flag = True
                else:
                    if lot_size:
                        data_flag = True
        if data_flag:
            ids = {}
            self.uid += 1
            args = (id[0], item['addressRegion'])
            # 用户信息表t_user-----------------------------------------
            user_sql, user_params = HouseImportOpt.get_sql_info_by_code(item, self.uid, "t_user", 1, *args,
                                                                        **ids)
            count = MysqlHelper.insert(user_sql, user_params)

            # 房源类型表 t_house_type----------------------------------------
            ids = {}
            args = ()
            type_temp_id = ()
            belongs = self.house_type_belongs(structure_type)
            # 数据库没有 则新增，房源类型图片目前以第一张房源图片作为URL， 后期需要UI提供
            if not belongs:
                # 数据库没匹配到
                self.house_type_id += 1
                house_type_sql, house_type_params = HouseImportOpt.get_sql_info_by_code(
                    item, self.house_type_id, "t_house_type", 2, *args, **ids)
                count = MysqlHelper.insert(house_type_sql, house_type_params)
            else:
                # 查询当前type_name的ID
                type_temp_id = MysqlHelper.get_one("select id from t_house_type where name = %s", [structure_type])

            # 房源数据表t_houses---------------------------------
            ids = {}
            args = ()
            city_id = id[0]
            type_id = ""
            if type_temp_id:
                type_id = type_temp_id[0]
            else:
                type_id = str(self.house_type_id)
            ids = {'user_id': str(self.uid), "city_id": city_id, "house_type_id": type_id}
            self.house_id += 1
            house_sql, house_params = HouseImportOpt.get_sql_info_by_code(item, self.house_id, "t_houses", 3, *args, **ids)
            count = MysqlHelper.insert(house_sql, house_params)

            # 房源辅图表t_house_img------------
            ids = {}
            row_count = 0
            for pic in pics:
                args = (self.house_id, pic)
                self.house_img_id += 1
                house_img_sql, house_img_params = HouseImportOpt.get_sql_info_by_code(
                    item, self.house_img_id, "t_house_img", 4, *args, **ids)
                count = MysqlHelper.insert(house_img_sql, house_img_params)
                row_count += count
            print(row_count)
        return item

    def close_spider(self, spider):
        MysqlHelper.close()
        # self.filename.close()
        # os.close()


