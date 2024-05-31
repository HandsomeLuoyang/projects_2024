# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import requests
from scrapy.pipelines.images import ImagesPipeline


class BmwPipeline(object):
    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)))
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def process_item(self, item, spider):
        category = item['category']
        urls = item['urls']

        category_path = os.path.join(self.path, category)
        if not os.path.exists(category_path):
            os.mkdir(category_path)
        for url in urls:
            imagename = url.split("_")[-1]
            with open(os.path.join(category_path, imagename), "wb") as wb:
                wb.write(requests.get(url=url).content)

        return item


class BMWImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        """在发送下载请求之前调用"""
        request_objs = super(BMWImagesPipeline, self).get_media_requests(item, info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None):
        """在图片将要被存储的时候调用，来获取这个图片的存储路径"""

        image_name = ImagesPipeline.file_path(self, request, response, info).split("/")[-1]

        category = request.item.get('category')

        category_path = category

        # if not os.path.exists(category_path):
        #     os.mkdir(category_path)
        image_path = os.path.join(category_path, image_name)

        return image_path