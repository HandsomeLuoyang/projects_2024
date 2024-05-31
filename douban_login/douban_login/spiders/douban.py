# -*- coding: utf-8 -*-
import scrapy


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://www.douban.com/']
    login_url = 'https://accounts.douban.com/j/mobile/login/basic'

    def start_requests(self):
    
    def parse(self, response):
        form_data = {
            'ck': '',
            'name': '17872298450',
            'password': '5421920',
            'remember': 'True',
            'ticket': ''
        }
        yield scrapy.FormRequest(url=self.login_url, formdata=form_data,
                                 callback=self.parse_after_login)
    
    def parse_after_login(self, response):
        yield scrapy.Request(url='https://www.douban.com/', callback=self.download_html)
        
    def download_html(self, response):
        with open("test.html", "w") as wf:
            wf.write(response.text)
