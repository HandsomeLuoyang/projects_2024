# -*- coding: utf-8 -*-
import scrapy


class LstqSpider(scrapy.Spider):
    name = 'lstq'
    allowed_domains = ['tianqihoubao.com']
    start_urls = ['http://tianqihoubao.com/']

    def parse(self, response):
        pass
