# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ForsalecrawlItem(scrapy.Item):
    click_url = scrapy.Field()
    status = scrapy.Field()
    addressLocality = scrapy.Field()
    addressRegion = scrapy.Field()
    # 邮编
    postalCode = scrapy.Field()
    # 街道信息
    streetAddress = scrapy.Field()
    # city_id
    # cityId = scrapy.Field()
    # 风格 公寓 还是个人
    style = scrapy.Field()
    base_info = scrapy.Field()
    price = scrapy.Field()
    beds = scrapy.Field()
    baths = scrapy.Field()
    sqft = scrapy.Field()
    # 图片列表
    pics = scrapy.Field()
    # 描述
    des = scrapy.Field()
    # build_year
    build_year = scrapy.Field()
    # Structure Type house/farm农场
    structure_type = scrapy.Field()
    # 地段面积
    lot_size = scrapy.Field()
    # parking 停车位
    parking = scrapy.Field()
    # contactphone
    phone = scrapy.Field()
