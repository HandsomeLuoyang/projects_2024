# -*- coding: utf-8 -*-
import scrapy
from douban_top250.items import DoubanTop250Item


class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250?start=0']
    base_domain = 'https://movie.douban.com/top250'

    def parse(self, response):
        divs = response.xpath('//*[@id="content"]/div/div[1]/ol/li')
        for div in divs:
            name = div.xpath('.//div/div[2]/div[1]/a/span[1]/text()').get().strip()
            info = div.xpath('.//div/div[2]/div[2]/p[1]/text()').getall()
            info = "".join(info).strip()
            try:
                brief_introduction = div.xpath('.//div/div[2]/div[2]/p[2]/span[@class="inq"]/text()').get().strip()
            except:
                brief_introduction = "无简介"
            item = DoubanTop250Item(name=name, info=info, brief_introduction=brief_introduction)
            yield item
        
        next_url = response.xpath('//span[@class="next"]/a/@href').get()
        print("=" * 40)
        print(next_url)
        print("=" * 40)
        target_url = self.base_domain + next_url
        if not next_url:
            return
        else:
            print("=" * 40)
            print(target_url)
            print("=" * 40)
            yield scrapy.Request(url=target_url, callback=self.parse)