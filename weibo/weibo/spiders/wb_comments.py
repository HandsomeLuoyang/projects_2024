# -*- coding: utf-8 -*-
import scrapy
import json
from weibo.items import CommentItem


class WbCommentsSpider(scrapy.Spider):
    name = 'wb_comments'
    allowed_domains = ['m.weibo.cn']
    start_urls = [
        'https://m.weibo.cn/comments/hotflow?id=4623018589948537&mid=4623018589948537&max_id_type=0']

    def parse(self, response):
        js = json.loads(response.text)
        max_id = '&max_id=' + str(js['data']['max_id'])
        # TODO: 存储其它数据
        next_url = response.url + max_id
        print(next_url)
        yield scrapy.Request(url=response.url + max_id,
                             callback=self.parse_next)

    def parse_next(self, response):
        try:
            js = json.loads(response.text)

            for comment in js['data']['data']:
                comment_time = comment['created_at']
                text = comment['text']
                comment_people_id = comment['user']['id']
                comment_people_name = comment['user']['screen_name']
                comment_likes = comment['like_count']
                total_number = comment['total_number']
                item = CommentItem(comment_time=comment_time,
                                text=text,
                                comment_people_id=comment_people_id,
                                comment_people_name=comment_people_name,
                                comment_likes=comment_likes,
                                total_number=total_number)
                yield item
            max_id = "&max_id=" + str(js['data']['max_id'])
            max_id_type = '&max_id_type=' + str(js['data']['max_id_type'])
            print("=" * 40)
            print(max_id)
            print(max_id_type)
            print("=" * 40)
            yield scrapy.Request(url=self.start_urls[0] + max_id + max_id_type,
                                callback=self.parse_next)
        except Exception as ret:
            print("=" * 40)
            print("此处出错！%s" & ret)
            print("=" * 40)
