# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import concurrent.futures as cf
# TODO:异步存储数据库

class JianshuSpiderPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1",
                                    user="root",
                                    password="gerenyinsi160",
                                    database="jianshu")
        self.cursor = self.conn.cursor()
    
    def open_spider(self, spider):
        print("爬虫开始了" * 40)
    
    
    def process_item(self, item, spider):
        print("开始存储数据了"*40)
        print(item)
        if item['subjects'] != '':
            self.sql = 'insert into details values(0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
            self.cursor.execute(self.sql, [item['title'],
                            item['content'],
                            item['article_id'],
                            item['origin_url'],
                            item['author'],
                            item['avatar'],
                            item['pub_time'],
                            item['read_count'],
                            item['word_count'],
                            item['subjects']])
        else:
            self.sql = 'insert into details(id, title, content, article_id, origin_url, author, avatar, pub_time, read_count, word_count) values(0, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
            self.cursor.execute(self.sql, [item['title'],
                            item['content'],
                            item['article_id'],
                            item['origin_url'],
                            item['author'],
                            item['avatar'],
                            item['pub_time'],
                            item['read_count'],
                            item['word_count']])
        
        self.conn.commit()
        print("数据已存储！" * 40)
    
    def close_spider(self, spider):
        print("爬虫关闭了" * 40)
        self.cursor.close()
        self.conn.close()