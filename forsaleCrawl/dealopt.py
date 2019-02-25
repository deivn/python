#! /usr/bin/env python  
# -*- coding:utf-8 -*-
import re
import math
import time
from decimal import *
from forsaleCrawl.sqlutil import SqlUtil


class HouseImportOpt(object):

    def __init__(self):
        pass

    @staticmethod
    def get_sql_info_by_code(item, id, tab_name, code, *args, **ids):
        """
        功能：根据表名，字段列表，生成sql语句
        :param tab_name: 表名
        :param item: 网页爬取的信息
        :return:
        """
        _fields = HouseImportOpt().get_fields_by_code(code)
        sql = SqlUtil.gen_sql_sql(tab_name, _fields)
        params = HouseImportOpt().get_params_by_user_item(item, code, id, *args, **ids)
        return (sql, params)

    def get_fields_by_code(self, code):
        """
        功能：根据code生成对应表的字段列表
        :param code: 字段标识code =1（用户表） 2 房源类型表 3 房源表 4 房源辅图表
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
        elif code == 3:
            _fields = ['id', 'user_id', 'state_id', 'city_name', 'city_id', 'house_type_id', 'price',
                       'property_price', 'apn', 'street', 'zip', 'bedroom', 'bathroom',
                       'lot_sqft', 'user_input_unit', 'living_sqft', 'latitude', 'longitude',
                       'year_build', 'img_url', 'remark', 'origin', 'release_type', 'check_status', 'shelf_status',
                        'contact_name', 'contact_phone', 'contact_email', 'create_time']
        elif code == 4:
            _fields = ['id', 'houses_id', 'img_url', 'level', 'type', 'create_time']
        return _fields

    def get_params_by_user_item(self, item, code, id, *args, **ids):
        """
        功能：根据用户item生成数据库表的参数列表
        :param item:
        :param code:1用户表参数 2房源类型表参数 3 房源表参数 4 房源辅图表参数
        :param id: primary key
        :param ids: 房源数据里要用到各个要关联的外键ID
        :return:
        """
        params = []
        create_time = math.floor(time.time())
        if code == 1:
            # 当前时间 yyyy-MM-dd HH:mm:ss
            current_time = SqlUtil.gen_current_time()
            state_id, city_id = args
            params = [id, item['phone'], ' ', ' ', ' ', ' ', ' ', ' ',
                      3, 1, ' ', 1, 1, 1, state_id, city_id,
                      item['streetAddress'], item['postalCode'], ' ', ' ', current_time]
        elif code == 2:
            name = item['structure_type']
            # if_belongs = self.house_type_belongs(name)
            # 数据库没有
            # 取图片列表第一张
            img_url = item['pics'][0] if len(item['pics']) else ''
            params = [id, name, 1, img_url, create_time]
        elif code == 3:
            user_id = ids['user_id']
            city_id = ids['city_id']
            house_type_id = ids['house_type_id']
            # city_namne
            city_name = item['addressLocality']
            price = item['price'].replace("$", "").replace(",", "")
            # 物业费无
            property_price = 0
            apn = ''
            # 邮编
            zip = item['postalCode']
            # state_id
            state_id = item['addressRegion']
            # GLEN SHIRE CT,Las Vegas, NV,7209
            street = item['streetAddress'] + ',' + city_name + ',' + ' '+state_id+' ' + zip

            # 卧室数量
            bedroom = item['beds']
            # 浴室数量
            bathroom = item['baths'].replace(" baths", "")
            # 占地面积  爬到的数据固定是英亩单位，这里转换为英尺sqft
            lot_sqft = item['lot_size']
            # 带单位的sqft
            user_input_unit = str(lot_sqft) + "sqft"
            # 居住面积
            living_sqft = item['sqft'].replace(",", "").replace("sqft", "")
            # 纬度
            latitude = 0
            # 经度
            longitude = 0
            # 建设年份
            year_build = item['build_year']
            # img_url 主图，使用图片列表中的第一张
            img_url = item['pics'][0] if len(item['pics']) else ""
            # remark 房源描述信息
            remark = item['des']
            # origin 来源:1.pc,2.wap,3.ios,4.Android  这里统一成pc
            orgin = 1
            # release_type 发布类型:1.出售,2.整租，3合租 统一是出售
            release_type = 1
            # check_status 审核状态:1.审核中,2.已审核,3.审核失败
            check_status = 1
            # shelf_status 上架状态:1.上架,2.下架，3删除
            shelf_status = 1
            # contact_name 联系人名称
            contact_name = ""
            # contact_phone 联系人电话
            contact_phone = item['phone']
            # contact_email 联系人邮箱
            contact_email = ""
            params = [id, user_id, state_id, city_name, city_id, house_type_id,
                      price, property_price, apn, street, zip, bedroom, bathroom,
                      lot_sqft, user_input_unit, living_sqft, latitude, longitude,
                      year_build, img_url, remark, orgin, release_type, check_status,
                      shelf_status, contact_name, contact_phone, contact_email, create_time
                      ]
        elif code == 4:
            house_id, pic = args
            params = [id, house_id, pic, 0, 1, create_time]
        return params

    @staticmethod
    def get_column_field(structure_type):
        if structure_type == 'Townhome':
            structure_type = 'Town house'
        elif structure_type == 'Multi':
            structure_type = 'Multiple'
        elif structure_type == 'Condo':
            structure_type = 'Condos/co-ops'
        elif structure_type == 'Farm':
            structure_type = 'Lots/Land'
        elif structure_type == 'SingleFamily':
            structure_type = 'Single family'
        return structure_type