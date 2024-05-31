# -*- coding: utf-8 -*-
import scrapy
import datetime
import requests
import re
from lxml import etree
from caipiao_500.items import YaItem, OuItem


class CpCrawlerSpider(scrapy.Spider):
    name = 'cp_crawler'
    allowed_domains = ['500.com']

    # start_urls = ['http://500.com/']

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',

    }

    def start_requests(self):
        list_url = 'https://live.500.com/wanchang.php?e={}'
        start_time = datetime.date(2015, 1, 1)
        end_time = datetime.date(2015, 3, 1)
        for i in range((end_time - start_time).days + 1):
            day = start_time + datetime.timedelta(days=i)
            url = list_url.format(day)
            yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_list(self, response):
        year = response.url.split('=')[-1].split('-')[0]
        trs = response.xpath('//table[@class="bf_tablelist01"]/tbody/tr')
        for tr in trs:
            if tr.xpath('./@style').get():
                continue
            wanchang = tr.xpath('./td[4]/span/text()').get()
            if '完' not in wanchang:
                continue
            saishi = tr.xpath('./td[1]/a/text()').get()
            lunci = tr.xpath('./td[2]/text()').get()
            cm_time = year + ' ' + tr.xpath('./td[3]/text()').get()
            zhudui = tr.xpath('./td[5]/a/span/text()').get()
            kedui = tr.xpath('./td[7]/a/span/text()').get()
            score = '-'.join([tr.xpath('./td[6]/div/a[1]/text()').get(), tr.xpath('./td[6]/div/a[3]/text()').get()])
            banchang_score = tr.xpath('./td[8]/text()').get()

            ya_url = tr.xpath('./td[9]/a[2]/@href').get()
            ou_url = tr.xpath('./td[9]/a[3]/@href').get()

            if 'http' not in ya_url and 'https' not in ya_url:
                ya_url = 'https:' + ya_url
            if 'http' not in ou_url and 'https' not in ou_url:
                ou_url = 'https:' + ou_url

            print(ya_url, ou_url)
            # print(saishi, lunci, cm_time,
            #       zhudui, kedui, score, banchang_score)
            # print(ya_url, ou_url)

            yield scrapy.Request(url=ya_url, callback=self.parse_ya_url,
                                 meta={'saishi': saishi, 'lunci': lunci, 'cm_time': cm_time,
                                       'zhudui': zhudui, 'kedui': kedui,
                                       'score': score, 'banchang_score': banchang_score})

            yield scrapy.Request(url=ou_url, callback=self.parse_ou_url,
                                 meta={'saishi': saishi, 'lunci': lunci, 'cm_time': cm_time,
                                       'zhudui': zhudui, 'kedui': kedui,
                                       'score': score, 'banchang_score': banchang_score})

    def parse_ya_url(self, response):
        # print(response.url)
        # with open('r.html', 'w') as wf:
        #     wf.write(response.text)
        trs = response.xpath('//table[@id="datatb"]/tr')
        for tr in trs[:15]:
            gongsi = tr.xpath('./td[2]/p/a/span[1]/text()').get()
            jishi_pan = ' '.join(
                tr.xpath('./td[3]/table/tbody/tr/td/text()').getall())
            jishi_time = tr.xpath('./td[4]/time/text()').get()
            chushi_pan = ' '.join(
                tr.xpath('./td[5]/table/tbody/tr/td/text()').getall())
            chushi_time = tr.xpath('./td[6]/time/text()').get()

            item = YaItem(saishi=response.meta['saishi'], lunci=response.meta['lunci'],
                          cm_time=response.meta['cm_time'], zhudui=response.meta['zhudui'],
                          kedui=response.meta['kedui'], score=response.meta['score'],
                          banchang_score=response.meta['banchang_score'], gongsi=gongsi,
                          jishi_pan=jishi_pan, jishi_time=jishi_time,
                          chushi_pan=chushi_pan, chushi_time=chushi_time)
            yield item
            # print(gongsi, jishi_pan, jishi_time, chushi_pan, chushi_time)

        # u_id = re.search('-(\d+?)\.', response.url).group(1)
        # index = 30
        # while True:
        #     ajax_url = 'http://odds.500.com/fenxi1/yazhi.php?id={}&ctype=1&start={}'.format(u_id, index)
        #     r = requests.get(url=ajax_url, headers=self.headers)
        #     if r.status_code != 200 or len(r.text) < 30:
        #         break
        #     index += 30
        #     html = etree.HTML(r.content.decode('utf8'))
        #     trs = html.xpath('//tr[@class="tr2"]')
        #     for tr in trs:
        #         gongsi = tr.xpath('./td[2]/p/a/span[1]/text()')[0]
        #         jishi_pan = ' '.join(tr.xpath('./td[3]/table/tbody/tr/td/text()'))
        #         jishi_time = tr.xpath('./td[4]/time/text()')[0]
        #         chushi_pan = ' '.join(tr.xpath('./td[5]/table/tbody/tr/td/text()'))
        #         chushi_time = tr.xpath('./td[6]/time/text()')[0]
        #
        #         item = YaItem(saishi=response.meta['saishi'], lunci=response.meta['lunci'],
        #                       cm_time=response.meta['cm_time'], zhudui=response.meta['zhudui'],
        #                       kedui=response.meta['kedui'], score=response.meta['score'],
        #                       banchang_score=response.meta['banchang_score'], gongsi=gongsi,
        #                       jishi_pan=jishi_pan, jishi_time=jishi_time,
        #                       chushi_pan=chushi_pan, chushi_time=chushi_time)
        #         yield item

        # print(gongsi, jishi_pan, jishi_time, chushi_pan, chushi_time)

    def parse_ou_url(self, response):
        trs = response.xpath('//table[@id="datatb"]/tr')[:-1]
        for tr in trs:
            gongsi = tr.xpath(
                './td[2]/p//span[@class="quancheng"]/text()').get()
            # print(gongsi)
            if '威廉希尔' not in gongsi and 'Bet365' not in gongsi:
                continue
            jishi_pei = tr.xpath('./td[3]/table/tbody/tr/td/text()').getall()
            qian_jishi_pei = jishi_pei[0] + ' ' + \
                             jishi_pei[1] + ' ' + jishi_pei[2]
            hou_jishi_pei = jishi_pei[3] + ' ' + \
                            jishi_pei[4] + ' ' + jishi_pei[5]

            jishi_gailv = tr.xpath('./td[4]/table/tbody/tr/td/text()').getall()
            qian_jishi_gailv = jishi_gailv[0] + ' ' + \
                               jishi_gailv[1] + ' ' + jishi_gailv[2]
            hou_jishi_gailv = jishi_gailv[3] + ' ' + \
                              jishi_gailv[4] + ' ' + jishi_gailv[5]

            # fanhuan = tr.xpath('./td[5]/table/tbody/tr/td/text()').getall()
            # qian_fanhuan, hou_fanhuan = fanhuan
            #
            # jishi_kaili = tr.xpath('./td[6]/table/tbody/tr/td/text()').getall()
            # qian_jishi_kaili = jishi_kaili[0] + ' ' + jishi_kaili[1] + ' ' + jishi_kaili[2]
            # hou_jishi_kaili = jishi_kaili[3] + ' ' + jishi_kaili[4] + ' ' + jishi_kaili[5]

            item = OuItem(saishi=response.meta['saishi'], lunci=response.meta['lunci'],
                          cm_time=response.meta['cm_time'], zhudui=response.meta['zhudui'],
                          kedui=response.meta['kedui'], score=response.meta['score'],
                          gongsi=gongsi, qian_hou='前', jishi_pei=qian_jishi_pei,
                          banchang_score=response.meta['banchang_score'],
                          jishi_gailv=qian_jishi_gailv)
            yield item

            item = OuItem(saishi=response.meta['saishi'], lunci=response.meta['lunci'],
                          cm_time=response.meta['cm_time'], zhudui=response.meta['zhudui'],
                          kedui=response.meta['kedui'], score=response.meta['score'],
                          gongsi=gongsi, qian_hou='前', jishi_pei=qian_jishi_pei,
                          banchang_score=response.meta['banchang_score'],
                          jishi_gailv=qian_jishi_gailv)
            yield item

            # print(gongsi, jishi_pei, jishi_gailv, fanhuan, jishi_kaili)
            # print(qian_jishi_pei)

        # u_id = re.search('-(\d+?)\.', response.url).group(1)
        # index = 30
        # while True:
        #     ajax_url = 'http://odds.500.com/fenxi1/ouzhi.php?id={}&ctype=1&start={}'.format(u_id, index)
        #     r = requests.get(url=ajax_url, headers=self.headers)
        #     if r.status_code != 200 or 'tr' not in r.text:
        #         break
        #     index += 30
        #     html = etree.HTML(r.content.decode('utf8'))
        #     trs = html.xpath('//tr[@class="tr1"]')
        #     for tr in trs:
        #         gongsi = tr.xpath('./td[2]/p//span[@class="quancheng"]/text()')[0]
        #         # print(gongsi)
        #         if '威廉希尔' not in gongsi and 'Bet365' not in gongsi:
        #             continue
        #         jishi_pei = tr.xpath('./td[3]/table/tbody/tr/td/text()')
        #         qian_jishi_pei = jishi_pei[0] + ' ' + jishi_pei[1] + ' ' + jishi_pei[2]
        #         hou_jishi_pei = jishi_pei[3] + ' ' + jishi_pei[4] + ' ' + jishi_pei[5]

        #         jishi_gailv = tr.xpath('./td[4]/table/tbody/tr/td/text()')
        #         qian_jishi_gailv = jishi_gailv[0] + ' ' + jishi_gailv[1] + ' ' + jishi_gailv[2]
        #         hou_jishi_gailv = jishi_gailv[3] + ' ' + jishi_gailv[4] + ' ' + jishi_gailv[5]

        #         # fanhuan = tr.xpath('./td[5]/table/tbody/tr/td/text()')
        #         # qian_fanhuan, hou_fanhuan = fanhuan
        #         #
        #         # jishi_kaili = tr.xpath('./td[6]/table/tbody/tr/td/text()')
        #         # qian_jishi_kaili = jishi_kaili[0] + ' ' + jishi_kaili[1] + ' ' + jishi_kaili[2]
        #         # hou_jishi_kaili = jishi_kaili[3] + ' ' + jishi_kaili[4] + ' ' + jishi_kaili[5]

        #         # print(gongsi, jishi_pei, jishi_gailv, fanhuan, jishi_kaili)

        #         item = OuItem(saishi=response.meta['saishi'], lunci=response.meta['lunci'],
        #                       cm_time=response.meta['cm_time'], zhudui=response.meta['zhudui'],
        #                       kedui=response.meta['kedui'], score=response.meta['score'],
        #                       gongsi=gongsi, qian_hou='前', jishi_pei=qian_jishi_pei,
        #                       jishi_gailv=qian_jishi_gailv)
        #         yield item

        #         item = OuItem(saishi=response.meta['saishi'], lunci=response.meta['lunci'],
        #                       cm_time=response.meta['cm_time'], zhudui=response.meta['zhudui'],
        #                       kedui=response.meta['kedui'], score=response.meta['score'],
        #                       gongsi=gongsi, qian_hou='后', jishi_pei=hou_jishi_pei,
        #                       jishi_gailv=hou_jishi_gailv)
        #         yield item
