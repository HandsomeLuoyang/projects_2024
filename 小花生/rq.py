# 本代码共有三个版本，分别为1.单线程版 2.线程池版 3.gevent协程版

# 网络请求库
import requests
# 网页结构处理库
from lxml import etree
# json数据处理库
import json

import time
# 正则库
import re
# csv文件库
import csv
# 线程池
from concurrent.futures import ThreadPoolExecutor

import gevent
from gevent import monkey
monkey.patch_all()

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'Accept': '*/*',
}

# 属性值=年龄对照表
code_age_map = {
    '1': '0-2岁',
    '2': '3-6岁',
    '3': '7-10岁',
    '4': '11岁+',
}

# 属性值-分类对照表
code_char_map = {
    '141': '必读',
    '140': '英语',
    '131': '启蒙认知',
    '139': '成长',
    '132': '文学',
    '133': '科普',
    '134': '艺术',
    '135': '历史',
    '138': '游戏',
    '143': '绘本',
    '146': '认识世界',
    '144': '中国文化',
}


# 书单列表json接口
url = 'https://www.xiaohuasheng.cn/Home/ReadingRecommendLoadMore'

# 书籍列表json接口
book_list_url = 'https://www.xiaohuasheng.cn/Read/BooklistBookLoadMore'

# 线程池，10个线程
threadPool = ThreadPoolExecutor(max_workers=10)

# 将要放到线程池里面的函数
def send_request(url, item1, item2):
    """
    url: 请求的链接
    item1: 年龄阶段
    item2: 书籍分类
    请求书籍详情页并存储信息到csv文件当中
    """
    try:
        print(url)
        # 发起网络get请求
        r1 = requests.get(url, headers=headers)
        # 将请求到的页面放入HTML中分析
        html_2 = etree.HTML(r1.text)
        
        # 通过xpath提取所需数据
        title = html_2.xpath(
            "//div[contains(@class, 'single_book_title')]/text()")[0]

        first_tag = html_2.xpath(
            "//div[contains(@class, 'app_book_info')]/div[1]/span/text()")[0]
        author = html_2.xpath(
            "//div[contains(@class, 'app_book_info')]/div[1]/text()")

        intro = html_2.xpath(
            "//span[@id='bookDescriptionLong']/text()")

        # 数据例外处理
        if '作者' not in first_tag:
            author = '无作者'
        else:
            author = author[1]

        if not intro:
            intro = '无简介'
        else:
            intro = intro[0]

        # print(title, author, intro)
        # print(author)
        # print(url)
        # 保存到csv文件当中
        with open('{}---{}.csv'.format(item1, item2), 'a', encoding='utf-8_sig') as af:
            csv_writer = csv.writer(af)
            csv_writer.writerow(
                [title, author, intro, url])

    # 错误日志记录
    except Exception as e:
        with open('error_logs.txt', 'a', encoding='utf8') as af:
            af.write(str(url)+':'+str(e)+'\n')
    

# 两个迭代循坏形成所有年龄和书籍分类的组合
for item1 in code_age_map.items():
    for item2 in code_char_map.items():
        # 生成年龄---分类的csv文件
        with open('{}---{}.csv'.format(item1[1], item2[1]), 'a', encoding='utf-8_sig') as af:
            csv_writer = csv.writer(af)
            csv_writer.writerow(['标题', '作者', '图书简介', '链接'])
        print(item1[1], item2[1])
        
        # json接口所需post的参数
        data = {
            'age': item1[0],
            'category': item2[0],
            'offset': '0',
            'limit': '100',
        }
        
        # 请求json接口
        r = requests.post(url=url, data=data, headers=headers)
        try:
            js = json.loads(r.text)
        except Exception as e:
            print(e)
            print(url)
        
        # 如果请求到的数据条数不为0
        if js[1] != '0':
            html = etree.HTML(js[0])
            # 从页面中获取所有的链接
            a_list = html.xpath('//a/@href')
            # 提取出链接的id，后续请求只需要用到id
            id_list = list(map(lambda x: re.search(r'\d+', x).group(), a_list))
            # 对每个id封装到数据中进行请求
            for _id in id_list:
                # 构造请求数据，这个网站反爬措施不强，一次可以请求10000个，基本包括所有的数据
                list_data = {'offset': '0',
                             'booklistId': str(_id), 'limit': '10000'}
                # 获取请求内容并转成json格式
                list_json = requests.post(
                    url=book_list_url, data=list_data, headers=headers).json()
                # 如果数据条数不为0
                if list_json[1] != '0':
                    html_1 = etree.HTML(list_json[0])
                    detail_list = html_1.xpath('//a/@href')

                    detail_list = list(
                        map(lambda x: 'https://www.xiaohuasheng.cn' + x, set(detail_list)))
                    
                    
                    task_list = []
                    for url_1 in detail_list:
                        # 对每个链接放入线程池中进行爬取
                        # time.sleep(0.1)
                        # threadPool.submit(send_request, url_1, item1[1], item2[1])
                        print(detail_list.index(url_1))
                        task = gevent.spawn(send_request, url_1, item1[1], item2[1])
                        task_list.append(task)
                    gevent.joinall(task_list)

# 等待内部所有线程执行完之后关闭线程池
# threadPool.shutdown(wait=True)

                        # try:
                        #     r = requests.get(url, headers=headers)
                        #     html_2 = etree.HTML(r.text)

                        #     title = html_2.xpath(
                        #         "//div[contains(@class, 'single_book_title')]/text()")[0]
                            
                        #     first_tag = html_2.xpath("//div[contains(@class, 'app_book_info')]/div[1]/span/text()")[0]
                        #     author = html_2.xpath(
                        #         "//div[contains(@class, 'app_book_info')]/div[1]/text()")

                        #     intro = html_2.xpath(
                        #         "//span[@id='bookDescriptionLong']/text()")
                            

                        #     if '作者' not in first_tag:
                        #         author = '无作者'
                        #     else:
                        #         author = author[1]

                        #     if not intro:
                        #         intro = '无简介'
                        #     else:
                        #         intro = intro[0]

                        #     # print(title, author, intro)
                        #     with open('{}---{}.csv'.format(item1[1], item2[1]), 'a', encoding='utf-8_sig') as af:
                        #         csv_writer = csv.writer(af)
                        #         csv_writer.writerow([title, author, intro, url])
                        # except Exception as e:
                        #     with open('error_logs.txt', 'a') as af:
                        #         af.write(str(url)+':'+str(e)+'\n')
