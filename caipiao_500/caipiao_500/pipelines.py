# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from caipiao_500.items import YaItem, OuItem
from scrapy.exporters import CsvItemExporter


class Caipiao500Pipeline(object):
    def __init__(self):
        self.ya_file = open('ya_data2.csv', 'wb')
        self.ou_file = open('ou_data2.csv', 'wb')
        self.ya_csv_file = CsvItemExporter(self.ya_file)
        self.ou_csv_file = CsvItemExporter(self.ou_file)

        self.ya_csv_file.fields_to_export = ['saishi', 'lunci', 'cm_time', 'zhudui',
                                             'kedui', 'score', 'banchang_score',
                                             'gongsi', 'jishi_pan', 'jishi_time',
                                             'chushi_pan', 'chushi_time']

        self.ou_csv_file.fields_to_export = ['saishi', 'lunci', 'cm_time', 'zhudui',
                                             'kedui', 'score', 'banchang_score',
                                             'gongsi', 'qian_hou', 'jishi_pei', 'jishi_gailv']

        self.ya_csv_file.start_exporting()
        self.ou_csv_file.start_exporting()

    def process_item(self, item, spider):
        if isinstance(item, YaItem):
            self.ya_csv_file.export_item(item)
        else:
            self.ou_csv_file.export_item(item)

        return item

    def close_item(self, spider):
        print('存储成功')
        self.ya_csv_file.finish_exporting()
        self.ou_csv_file.finish_exporting()
        self.ya_file.close()
        self.ou_file.close()
