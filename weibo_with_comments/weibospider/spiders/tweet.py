#!/usr/bin/env python
# encoding: utf-8
"""
File Description: 
Author: nghuyong
Mail: nghuyong@163.com
Created Time: 2020/4/14
"""
import datetime
import re
from lxml import etree
from scrapy import Spider
from scrapy.http import Request
import time
from items import TweetItem
from urllib.parse import unquote
from spiders.utils import time_fix, extract_weibo_content


class TweetSpider(Spider):
    name = "tweet_spider"
    base_url = "https://weibo.cn"

    def start_requests(self):

        def init_url_by_user_id():
            # crawl tweets post by users
            # === change the following config ===
            user_ids = ['1087770692', '1699432410', '1266321801']
            # === change the above config ===
            urls = [f'{self.base_url}/{user_id}/profile?page=1' for user_id in user_ids]
            return urls

        def init_url_by_user_id_and_date():
            # crawl specific users' tweets in a specific date
            # === change the following config ===
            user_ids = ['1699432410']
            start_date = datetime.datetime.strptime("2020-01-01", '%Y-%m-%d')
            end_date = datetime.datetime.strptime("2020-12-31", '%Y-%m-%d')
            # === change the above config ===
            time_spread = datetime.timedelta(days=20)
            url_format = "https://weibo.cn/{}/profile?hasori=0&haspic=0&starttime={}&endtime={}&advancedfilter=1&page=1"
            urls = []
            while start_date < end_date:
                for user_id in user_ids:
                    start_date_string = start_date.strftime("%Y%m%d")
                    tmp_end_date = start_date + time_spread
                    if tmp_end_date >= end_date:
                        tmp_end_date = end_date
                    end_date_string = tmp_end_date.strftime("%Y%m%d")
                    urls.append(url_format.format(user_id, start_date_string, end_date_string))
                start_date = start_date + time_spread
            return urls
        
        def init_url_by_user_id_and_date_and_keywords():
            # crawl specific users' tweets in a specific date and keyword
            # === change the following config ===
            user_ids = ['1699432410']
            keywords= ['新冠']
            start_date = datetime.datetime.strptime("2020-01-01", '%Y-%m-%d')
            end_date = datetime.datetime.strptime("2020-12-31", '%Y-%m-%d')
            # === change the above config ===
            time_spread = datetime.timedelta(days=1)
            url_format = "https://weibo.cn/{}/profile?keyword={}&hasori=0&haspic=0&starttime={}&endtime={}&advancedfilter=1&page=1"
            urls = []
            while start_date < end_date:
                for user_id in user_ids:
                    for keyword in keywords:
                        start_date_string = start_date.strftime("%Y%m%d")
                        tmp_end_date = start_date + time_spread
                        if tmp_end_date >= end_date:
                            tmp_end_date = end_date
                        end_date_string = tmp_end_date.strftime("%Y%m%d")
                        urls.append(url_format.format(user_id, keyword, start_date_string, end_date_string))
                start_date = start_date + time_spread
            return urls

        def init_url_by_keywords_and_date():
            # crawl tweets include keywords in a period, you can change the following keywords and date
            # === change the following config ===
            keywords = ['北京']
            start_date = datetime.datetime.strptime("2021-01-01", '%Y-%m-%d')
            end_date = datetime.datetime.strptime("2021-01-02", '%Y-%m-%d')
            # === change the above config ===
            time_spread = datetime.timedelta(days=1)
            url_format = "https://weibo.cn/search/mblog?hideSearchFrame=&keyword={}&starttime={}&endtime={}&atten=1&sort=time&page=1"
            urls = []
            while start_date <= end_date:
                for keyword in keywords:
                    # 添加按日的url
                    day_string = start_date.strftime("%Y%m%d")
                    urls.append(url_format.format(keyword, day_string, day_string))
                start_date = start_date + time_spread
            return urls

        # select urls generation by the following code
        # urls = init_url_by_user_id()
        # urls = init_url_by_keywords_and_date()
        # urls = init_url_by_user_id_and_date()
        urls = init_url_by_user_id_and_date_and_keywords()
        for url in urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        if response.url.endswith('page=1'):
            all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
            if all_page:
                all_page = all_page.group(1)
                all_page = int(all_page)
                for page_num in range(2, all_page + 1):
                    page_url = response.url.replace('page=1', 'page={}'.format(page_num))
                    yield Request(page_url, self.parse, dont_filter=True, meta=response.meta)
                # 如果是搜索接口，按照天的粒度结果已经是100页，那继续按照小时的粒度进行切分
                if 'search/mblog' in response.url and all_page == 100 and '-' not in response.url:
                    start_time_string = re.search(r'starttime=(\d+)&', unquote(response.url, "utf-8")).group(1)
                    keyword = re.search(r'keyword=(.*?)&', unquote(response.url, "utf-8")).group(1)
                    self.logger.info(f'split by hour,{start_time_string},{keyword}, {unquote(response.url, "utf-8")}')
                    date_start = datetime.datetime.strptime(start_time_string, "%Y%m%d")
                    time_spread = datetime.timedelta(days=1)
                    url_format_by_hour = "https://weibo.cn/search/mblog?hideSearchFrame=&keyword={}&advancedfilter=1&starttime={}&endtime={}&sort=time&atten=1&page=1"
                    one_day_back = date_start - time_spread
                    # from today's 7:00-8:00am to 23:00-24:00am
                    for hour in range(7, 24):
                        # calculation rule of starting time: start_date 8:00am + offset:16
                        begin_hour = one_day_back.strftime("%Y%m%d") + "-" + str(hour + 16)
                        # calculation rule of ending time: (end_date+1) 8:00am + offset:-7
                        end_hour = one_day_back.strftime("%Y%m%d") + "-" + str(hour - 7)
                        page_url = url_format_by_hour.format(keyword, begin_hour, end_hour)
                        yield Request(page_url, self.parse, dont_filter=True, meta=response.meta)
                    two_day_back = one_day_back - time_spread
                    # from today's 0:00-1:00am to 6:00-7:00am
                    for hour in range(0, 7):
                        # note the offset change bc we are two-days back now
                        begin_hour = two_day_back.strftime("%Y%m%d") + "-" + str(hour + 40)
                        end_hour = two_day_back.strftime("%Y%m%d") + "-" + str(hour + 17)
                        page_url = url_format_by_hour.format(keyword, begin_hour, end_hour)
                        yield Request(page_url, self.parse, dont_filter=True, meta=response.meta)

        tree_node = etree.HTML(response.body)
        tweet_nodes = tree_node.xpath('//div[@class="c" and @id]')
        for tweet_node in tweet_nodes:
            try:
                tweet_item = TweetItem()
                tweet_item['crawl_time'] = int(time.time())
                tweet_repost_url = tweet_node.xpath('.//a[contains(text(),"转发[")]/@href')[0]
                user_tweet_id = re.search(r'/repost/(.*?)\?uid=(\d+)', tweet_repost_url)
                tweet_item['weibo_url'] = 'https://weibo.com/{}/{}'.format(user_tweet_id.group(2),
                                                                           user_tweet_id.group(1))
                tweet_item['user_id'] = user_tweet_id.group(2)
                tweet_item['_id'] = user_tweet_id.group(1)
                create_time_info_node = tweet_node.xpath('.//span[@class="ct"]')[-1]
                create_time_info = create_time_info_node.xpath('string(.)')
                if "来自" in create_time_info:
                    tweet_item['created_at'] = time_fix(create_time_info.split('来自')[0].strip())
                    tweet_item['tool'] = create_time_info.split('来自')[1].strip()
                else:
                    tweet_item['created_at'] = time_fix(create_time_info.strip())

                like_num = tweet_node.xpath('.//a[contains(text(),"赞[")]/text()')[-1]
                tweet_item['like_num'] = int(re.search('\d+', like_num).group())

                repost_num = tweet_node.xpath('.//a[contains(text(),"转发[")]/text()')[-1]
                tweet_item['repost_num'] = int(re.search('\d+', repost_num).group())

                comment_num = tweet_node.xpath(
                    './/a[contains(text(),"评论[") and not(contains(text(),"原文"))]/text()')[-1]
                tweet_item['comment_num'] = int(re.search('\d+', comment_num).group())

                images = tweet_node.xpath('.//img[@alt="图片"]/@src')
                if images:
                    tweet_item['image_url'] = images

                videos = tweet_node.xpath('.//a[contains(@href,"https://m.weibo.cn/s/video/show?object_id=")]/@href')
                if videos:
                    tweet_item['video_url'] = videos

                map_node = tweet_node.xpath('.//a[contains(text(),"显示地图")]')
                if map_node:
                    map_node = map_node[0]
                    map_node_url = map_node.xpath('./@href')[0]
                    map_info = re.search(r'xy=(.*?)&', map_node_url).group(1)
                    tweet_item['location_map_info'] = map_info

                repost_node = tweet_node.xpath('.//a[contains(text(),"原文评论[")]/@href')
                if repost_node:
                    tweet_item['origin_weibo'] = repost_node[0]

                all_content_link = tweet_node.xpath('.//a[text()="全文" and contains(@href,"ckAll=1")]')
                if all_content_link:
                    all_content_url = self.base_url + all_content_link[0].xpath('./@href')[0]
                    yield Request(all_content_url, callback=self.parse_all_content, meta={'item': tweet_item},
                                  priority=1)
                else:
                    tweet_html = etree.tostring(tweet_node, encoding='unicode')
                    tweet_item['content'] = extract_weibo_content(tweet_html)
                    yield tweet_item

            except Exception as e:
                self.logger.error(e)

    def parse_all_content(self, response):
        tree_node = etree.HTML(response.body)
        tweet_item = response.meta['item']
        content_node = tree_node.xpath('//*[@id="M_"]/div[1]')[0]
        tweet_html = etree.tostring(content_node, encoding='unicode')
        tweet_item['content'] = extract_weibo_content(tweet_html)
        yield tweet_item
