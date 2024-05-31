# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exporters import JsonLinesItemExporter
from fang.items import NewHouseItem, ESFHouseItem

class FangPipeline(object):
    def __init__(self):
        self.new_house_fp = open("newhouse.json", "wb")
        self.esf_house_fp = open("esfhouse.json", "wb")
        self.newhouse_exporter = JsonLinesItemExporter(self.new_house_fp,
                                                       ensure_ascii=False)
        self.esfhouse_exporter = JsonLinesItemExporter(self.esf_house_fp,
                                                       ensure_ascii=False)
    
    def process_item(self, item, spider):
        if isinstance(item, NewHouseItem):
            self.newhouse_exporter.export_item(item)
        else:
            self.esfhouse_exporter.export_item(item)
        return item
    
    def close_spider(self, spider):
        self.new_house_fp.close()
        self.esf_house_fp.close()
