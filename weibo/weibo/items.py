# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CommentItem(scrapy.Item):
    '''评论item'''
    # 评论时间
    comment_time = scrapy.Field()
    # 评论文本
    text = scrapy.Field()
    # 评论人id
    comment_people_id = scrapy.Field()
    # 评论人name
    comment_people_name = scrapy.Field()
    # 评论点赞数
    comment_likes = scrapy.Field()
    # 评论回复总数
    total_number = scrapy.Field()

class PeopleItem(scrapy.Item):
    '''用户item'''
    # 用户昵称
    name = scrapy.Field()
    # 用户id
    user_id = scrapy.Field()
    # 关注数
    follow_count = scrapy.Field()
    # 粉丝数
    followers_count = scrapy.Field()
    # 描述
    description = scrapy.Field()
    # 微博数
    statuses_count = scrapy.Field()
    # 是否认证
    verified = scrapy.Field()
    # 认证缘由
    verified_reason = scrapy.Field()
    
    
class StatusesItem(scrapy.Item):
    '''微博item'''
    # 最后编辑于
    edit_at = scrapy.Field()
    # 文本
    text = scrapy.Field()
    # 转发数
    reposts_count = scrapy.Field()
    # 评论数
    comments_count = scrapy.Field()
    # 点赞数
    attitudes_count = scrapy.Field()
    # 微博id
    statues_id = scrapy.Field()
    # 详情页URL
    origin_url = scrapy.Field()