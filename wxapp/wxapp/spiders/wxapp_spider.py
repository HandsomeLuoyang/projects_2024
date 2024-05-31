# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wxapp.items import WxappItem


class WxappSpiderSpider(CrawlSpider):
    name = 'wxapp_spider'
    allowed_domains = ['wxapp-union.com']
    start_urls = ['http://www.wxapp-union.com/portal.php?mod=list&catid=2&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'.+list&catid=2&page=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'.+/article-.+\.html'), callback='parse_detail', follow=False)
    )

    def parse_detail(self, response):
        title = response.xpath('//h1[@class="ph"]/text()').get()
        author_p = response.xpath('//*[@id="ct"]/div[1]/div/div[1]/div/div[2]/div[3]/div[1]/p')
        author = author_p.xpath('.//a/text()').get()
        pub_time = author_p.xpath('.//span/text()').get()
        article_content = response.xpath('//*[@id="article_content"]//text()').getall()
        article_content = "".join(article_content).strip()
        item = WxappItem(title=title, author=author, pub_time=pub_time, content=article_content)
        yield item