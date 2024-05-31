# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
import time
from scrapy.http.response.html import HtmlResponse
from selenium.webdriver.chrome.options import Options
# TODO：设置无头谷歌


class SeleniumDownloadMiddleware(object):
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        
        self.driver = webdriver.Chrome(options=self.chrome_options)
    
    
    def process_request(self, request, spider):
        self.driver.get(request.url)
        self.driver.set_page_load_timeout(5)
        time.sleep(1)
        try:
            while True:
                showMore = self.driver.find_element_by_class_name('H7E3vT')
                showMore.click()
                time.sleep(0.3)
                if not showMore:
                    break
        except:
            pass
        
        source = self.driver.page_source
        response = HtmlResponse(self.driver.current_url, body=source,
                                request=request,
                                encoding="utf-8")
        return response