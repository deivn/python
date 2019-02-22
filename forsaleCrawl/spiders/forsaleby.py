# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from forsaleCrawl.items import ForsalecrawlItem
import re


class ForsalebySpider(Spider):
    name = 'forsaleby'
    allowed_domains = ['forsalebyowner.com']
    offset = 1
    start_urls = ["https://www.forsalebyowner.com/search/list/New%20York/"+str(offset)+"-page"]

    # rules = (
    #     Rule(LinkExtractor(allow=r'/listing/\d+-[A-za-z]\w+-[A-za-z]\w+-[A-za-z]\w+-NY/[A-za-z0-9]\w'),
    #          callback='parse_item'),
    # )

    def parse(self, response):
        # 当前页的所有要进入的链接
        links = response.xpath('//div[@class="estate-bd"]/a/@href').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_item)
        if self.offset <= 37:
            self.offset += 1
            yield scrapy.Request("https://www.forsalebyowner.com/search/list/New%20York/"+str(self.offset)+"-page",
                                 callback=self.parse)

    # 每一页的每个链接请求后的返回结果，即请求后的结果内容
    def parse_item(self, response):
        # 状态
        item = ForsalecrawlItem()
        item['click_url'] = response.url
        item['status'] = response.xpath('//div//strong[@class="text-danger"]/text()').extract()[0]
        # address = response.xpath('')
        item['addressLocality'] = response.xpath('//ul[@itemprop="address"]//li//span[@itemprop="addressLocality"]/text()').extract()[0]
        item['addressRegion'] = response.xpath('//ul[@itemprop="address"]//li//span[@itemprop="addressRegion"]/text()').extract()[0]
        item['postalCode'] = response.xpath('//ul[@itemprop="address"]//li//span[@itemprop="postalCode"]/text()').extract()[0]
        item['streetAddress'] = response.xpath('//ul[@itemprop="address"]//li//span[@itemprop="streetAddress"]/text()').extract()[0]
        cityId = re.search('(\d+)', item['streetAddress'])
        # 城市ID
        item['cityId'] = cityId.group() if cityId else ""
        # 风格 公寓 还是个人
        style = response.xpath('//ul/li[1]/span[@class="summary-list__label"]/text()').extract()[0]
        # Farm/Land
        item['style'] = style.replace("\n", "").replace(" ", "")
        base_info = response.xpath('//div[@class="summary-list__col col-2 col-md-5"]/ul[2]')
        item['price'] = base_info.xpath('./li[1]/label/text()').extract()[0]

        item['beds'] = base_info.xpath('./li[2]/label/span/text()').extract()[0].strip()
        try:
            item['baths'] = base_info.xpath('./li[3]/label/text()').extract()[0]
        except IndexError:
            pass
        item['sqft'] =base_info.xpath('./li[4]/label/text()').extract()[0].replace(".", "").replace(" ","")
        # 图片列表
        item['pics'] = response.css('img::attr(data-image)').extract()
        # 描述
        des = " ".join(response.xpath('//div[@class="box"]/div/div/text() | //div[@class="box-hd"]//p[1]/text() | //div[@class="box"]/div[@class="box-hd"]/div/p/text() | //div[@class="box"]/div[@class="box-hd"]/div/ul/li/text()').extract())
        if not des:
            print(des)
        item['des'] = des.replace("\n", "")
        exterior_features = "".join(response.xpath('//div[@class="cols details"][2]/ul/li/span/text()').extract())
        # Structure Type house/farm农场
        exterior_features = exterior_features.strip().replace("\n", "")
        # Structure Type: House
        structure_type = re.search("Structure Type:\s(\w+)", exterior_features)
        if structure_type:
            item['structure_type'] = structure_type.group(1)
        # 建造年份
        build_year = re.search("Built in:\s(\d+)", exterior_features)
        item['build_year'] = build_year.group(1) if build_year else ""
        # 地段面积
        lot_size = re.search("Lot Size:\s([0-9][\.]\d+\s\w+)", exterior_features)
        item['lot_size'] = lot_size.group(1) if lot_size else ""
        # parking 停车位
        parking = re.search("Parking:\s(\d+\sSpace)", exterior_features)
        item['parking'] = parking.group(1) if parking else ""
        # contactphone
        phome_xl = response.xpath('//div[@id="contact"]//strong/text()').extract()
        item['phone'] = phome_xl[0][0:-1] if len(phome_xl) > 0 else ""
        yield item
