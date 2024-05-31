# -*- coding: utf-8 -*-
import scrapy
import re
from fang.items import NewHouseItem, ESFHouseItem

class SfwSpider(scrapy.Spider):
    name = 'sfw'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        trs = response.xpath('//*[@id="senfe"]//tr')[:-1]
        province = None
        for tr in trs:
            tds = tr.xpath('.//td[not(@class)]')
            province_td = tds[0]
            province_text = province_td.xpath('.//text()').get()
            province_text = re.sub(r'\s', '', province_text)
            if province_text:
                province = province_text
            city_id = tds[1]
            city_links = city_id.xpath('.//a')
            for city_link in city_links:
                city  = city_link.xpath('.//text()').get()
                city_url = city_link.xpath('.//@href').get()
                # 构建新房url链接
                tem_url = city_url.split(".")
                newhouse_url = tem_url[0] + ".newhouse.fang.com/house/s"
                # 构建二手房url链接
                tem_url = city_url.split(".")
                esf_url = tem_url[0] + ".esf.fang.com/"
                
                yield scrapy.Request(url=newhouse_url,
                                     callback=self.parse_newhouse,
                                     meta={"info":(province, city)})
                yield scrapy.Request(url=esf_url, 
                                     callback=self.parse_esf, 
                                     meta={'info':(province, city)})
    
    def parse_newhouse(self, response):
        province, city = response.meta.get('info')
        lis = response.xpath('//div[@id="newhouse_loupai_list"]/ul/li')
        for li in lis:
            style = li.xpath('./@style').get()
            if style:
                continue
            
            name = li.xpath('.//div[@class="nlcd_name"]/a/text()').get().strip()
            house_type_list = li.xpath('.//div[contains(@class,"house_type")]/a/text()').getall()
            house_type_list = list(map(lambda x: re.sub(r"\s", "", x), house_type_list))
            rooms = list(filter(lambda x: x.endswith("居"), house_type_list))
            if rooms:
                rooms = "/".join(rooms)
            else:
                rooms = ""
            area = "".join(li.xpath('.//div[contains(@class,"house_type")]/text()').getall())
            area = re.sub(r"\s|－|/", "", area)
            address = li.xpath('.//div[@class="address"]/a/@title').get()
            district_text = "".join(li.xpath('.//div[@class="address"]/a//text()').getall())
            district = ""
            r = re.search(r".*\[(.+)\].*", district_text)
            if r:
                district = r.group(1)
            sale = li.xpath('.//div[contains(@class, "fangyuan")]/span/text()').get()               
            price = "".join(li.xpath('.//div[@class="nhouse_price"]//text()').getall())
            price = re.sub(r"\s", "", price)
            origin_url = "https:" + li.xpath('.//div[@class="nlcd_name"]/a/@href').get().split('?')[0]
               
            item = NewHouseItem(name=name, 
                                city=city,
                                price=price,
                                rooms=rooms,
                                province=province,
                                area=area,
                                address=address,
                                district=district,
                                sale=sale,
                                origin_url=origin_url
                                )
            yield item
            
        next_url = response.xpath('//a[@class="next"]/@href').get()
        if next_url:
            next_url = response.url + next_url.split('/')[-2]
            yield scrapy.Request(url=next_url, callback=self.parse_newhouse,
                                 meta={'info':(province, city)})
        
    def parse_esf(self, response):
        province, city = response.meta.get('info')
        
        dls = response.xpath('/html/body/div[3]/div[1]/div[4]/div[6]/dl')
        
        for dl in dls:
            # 跳过广告
            if dl.xpath('./@dataflag').get() != "bg":
                continue
            name = dl.xpath('.//span[@class="tit_shop"]/text()').get()
            detail_infos = dl.xpath('.//p[@class="tel_shop"]/text()').getall()
            detail_infos = '/'.join(list(map(lambda x: re.sub(r'\s', '', x), detail_infos)))
            
            address = '[' + dl.xpath('.//p[@class="add_shop"]/a/@title').get() + ']' + dl.xpath('.//p[@class="add_shop"]/span/text()').get()
            price = "".join(dl.xpath('.//dd[@class="price_right"]/span[1]//text()').getall()).strip()
            unit = dl.xpath('.//dd[@class="price_right"]/span[2]/text()').get()
            origin_url = "https://esf.fang.com" + dl.xpath('.//h4[@class="clearfix"]/a/@href').get()
            sale_people = dl.xpath('.//span[@class="people_name"]/a/text()').get()
            
            item = ESFHouseItem(name=name,
                                detail_infos=detail_infos,
                                address=address,
                                price=price,
                                unit=unit,
                                origin_url=origin_url,
                                sale_people=sale_people,
                                province=province,
                                city=city)
            yield item
        
        next_url = "https://esf.fang.com" + response.xpath('//div[@class="page_al"]/p[last()-2]/a/@href').get()
        
        yield scrapy.Request(url=next_url, callback=self.parse_esf,
                             meta={'info':(province, city)})
        
        
        