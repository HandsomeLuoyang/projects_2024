# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from weibo.items import PeopleItem, StatusesItem, CommentItem


from scrapy.exporters import JsonLinesItemExporter
class WeiboPipeline(object):
    def __init__(self):
        self.comments_fp = open("comments.json", "wb")
        self.people_fp = open('people.json', 'wb')
        self.statuses_fp = open('statuses.json', 'wb')
        self.comments_exporter = JsonLinesItemExporter(self.comments_fp,
                                              ensure_ascii=False)
        self.people_exporter = JsonLinesItemExporter(self.people_fp,
                                              ensure_ascii=False)
        self.statuses_exporter = JsonLinesItemExporter(self.statuses_fp,
                                              ensure_ascii=False)
    
    def process_item(self, item, spider):
        if isinstance(item, CommentItem):
            self.comments_exporter.export_item(item)
        elif isinstance(item, PeopleItem):
            self.people_exporter.export_item(item)
        else:
            self.statuses_exporter.export_item(item)
        
        return item

    def close_item(self, spider):
        print("存储成功！")
        self.comments_fp.close()
        self.people_fp.close()
        self.statuses_fp.close()