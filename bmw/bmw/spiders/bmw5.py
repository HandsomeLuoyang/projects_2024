# -*- coding: utf-8 -*-
import scrapy
from bmw.items import BmwItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Bmw5Spider(CrawlSpider):
    name = 'bmw5'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/65.html']
    rules = (
        Rule(LinkExtractor(allow="https://car.autohome.com.cn/pic/series/65.+"),
             callback="parse_page",
             follow=True),
    )

    def parse_page(self, response):
        category = response.xpath('/html/body/div[2]/div/div[2]/div[7]/div/div[2]/div[1]/text()').get()
        srcs = response.xpath('/html/body/div[2]/div/div[2]/div[7]/div/div[2]/div[2]/ul//img/@src').getall()
        srcs = list(map(lambda url: 'https:' + url.replace('240x180', '1920x1280'), srcs))
        item = BmwItem(category=category, image_urls=srcs)
        yield item
    
    
    
    
    
    
    def text_page(self, response):
        uiboxs = response.xpath('//div[@class="uibox"]')[1:]
        for uibox in uiboxs:
            ui_title = uibox.xpath('./div[1]/a/text()').get()
            urls = uibox.xpath('.//ul/li/a/img/@src').getall()
            urls = list(map(lambda url: 'https:' + url, urls))
            item = BmwItem(category=ui_title, image_urls=urls)
            yield item