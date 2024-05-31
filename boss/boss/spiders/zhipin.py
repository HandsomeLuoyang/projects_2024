# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ZhipinSpider(CrawlSpider):
    name = 'zhipin'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/c101010100/?query=python&page=1']

    rules = (
        # 匹配职位列表页的规则
        Rule(LinkExtractor(allow=r'.+\?query=python&page=\d+'),
             follow=False),
        Rule(LinkExtractor(allow=r'.+job_detail/.+'),
             callback='parse_job',
             follow=False)
    )

    def parse_job(self, response):
        title = response.xpath('//*[@id="main"]/div[1]/div/div/div[2]/div[2]/h1/text()').get().strip()
        # salary = response.xpath('//*[@id="main"]/div[1]/div/div/div[2]/div[2]/span/text()').get().strip()
        if title:
            print("=" * 40)
            print(title)    
