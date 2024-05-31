# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu_spider.items import ArticleSpiderItem


class JsSpider(CrawlSpider):
    name = 'js'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'),
             callback='parse_detail',
             follow=True),
    )

    def parse_detail(self, response):
        title = response.xpath('//*[@id="__next"]/div[1]/div/div/section[1]/h1/text()').get()
        author = response.xpath('//*[@id="__next"]/div[1]/div/div/section[1]/div[1]/div/div/div[1]/span/a/text()').get()
        pub_time = response.xpath('//*[@id="__next"]/div[1]/div/div/section[1]/div[1]/div/div/div[2]/time/text()').get().replace('.', '-')
        word_count = response.xpath('//*[@id="__next"]/div[1]/div/div/section[1]/div[1]/div/div/div[2]/span[2]/text()').get()
        read_count = response.xpath('//*[@id="__next"]/div[1]/div/div/section[1]/div[1]/div/div/div[2]/span[3]/text()').get()
        avatar = response.xpath('//*[@id="__next"]/div[1]/div/div/section[1]/div[1]/div/a/img/@src').get()
        
        url = response.url
        url1 = url.split("?")[0]
        article_id = url1.split("/")[-1]
        origin_url = response.url
        content = response.xpath('//*[@id="__next"]/div[1]/div/div[1]/section[1]/article').get()
        
        subjects_pre = response.xpath('//*[@id="__next"]/div[1]/div/div[1]/section[2]/div/a/span/text()').getall()
        if subjects_pre is not None:
            subjects = ",".join(subjects_pre)
        else:
            subjects = ''
        
        item = ArticleSpiderItem(title=title, author=author,
                                 pub_time=pub_time, word_count=word_count,
                                 read_count=read_count, avatar=avatar,
                                 article_id=article_id, origin_url=origin_url,
                                 content=content, subjects=subjects)
        yield item