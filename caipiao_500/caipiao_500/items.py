# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    saishi = scrapy.Field()
    lunci = scrapy.Field()
    cm_time = scrapy.Field()
    zhudui = scrapy.Field()
    kedui = scrapy.Field()
    score = scrapy.Field()
    banchang_score = scrapy.Field()
    gongsi = scrapy.Field()
    jishi_pan = scrapy.Field()
    jishi_time = scrapy.Field()
    chushi_pan = scrapy.Field()
    chushi_time = scrapy.Field()


class OuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    saishi = scrapy.Field()
    lunci = scrapy.Field()
    cm_time = scrapy.Field()
    zhudui = scrapy.Field()
    kedui = scrapy.Field()
    score = scrapy.Field()
    banchang_score = scrapy.Field()
    gongsi = scrapy.Field()
    jishi_pei = scrapy.Field()
    jishi_gailv = scrapy.Field()
    # fanhuan = scrapy.Field()
    # jishi_kaili = scrapy.Field()
    qian_hou = scrapy.Field()
