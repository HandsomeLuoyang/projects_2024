# coding:utf-8
import requests
from lxml import etree
import threading
import time
import csv
import random
import traceback
import re
from multiprocessing.pool import Pool

# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "H8FXR6BON934W42D"
proxyPass = "B831D140587AC769"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

proxies = {
    "http": proxyMeta
}

ua_list = [
    'User-Agent,Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'User-Agent,Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'User-Agent,Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'User-Agent,Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'User-Agent,Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'User-Agent, Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
    'User-Agent,Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
    'User-Agent,Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'User-Agent,Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'User-Agent, Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'User-Agent, Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
    'User-Agent, Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
    'User-Agent, Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'User-Agent, Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
    'User-Agent, Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'User-Agent, Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
    'User-Agent, Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
    'User-Agent, Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'User-Agent,Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36'
]

lock = threading.Lock()

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'Accept': ':text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9'}


def yisheng_detail(url):
    while True:
        try:
            headers['User-Agent'] = random.choice(ua_list)
            while True:
                r = requests.get(url=url, headers=headers)
                if r.status_code == 200:
                    break
                try:
                    headers['User-Agent'] = random.choice(ua_list)
                    r = requests.get(url=url, headers=headers, proxies=proxies, timeout=2)
                    time.sleep(2)
                except:
                    pass
                else:
                    break
            html = etree.HTML(r.text)
            name = html.xpath('//div[@class="ys09_body"]/dl/dd/ul/span/a/text()')[0].strip()
            touxian = html.xpath('//div[@class="ys09_body"]/dl/dd/ul/text()')[0].strip()
            disease_as = html.xpath('//div[@class="ys10b"]/ul/a')
            hospital_infos = html.xpath('//div[@class="ys09_body"]/dl/dd/ol/a/text()')[0]
            hospital_name = hospital_infos.split()[0]
            keshi_name = hospital_infos.split()[1]

        except Exception as ret:
            traceback.print_exc()
            print(url)
            print(r.status_code)
        else:
            try:
                intro = html.xpath('//ul[@class="ys10a"][1]/div/text()')[0].strip()
            except Exception as ret:
                intro = '暂无信息'
            try:
                good_at = html.xpath('//ul[@class="ys10a"][2]/text()')[0].strip()
            except:
                good_at = '暂无信息'

            break

    diseases = ''
    index = 1

    if disease_as:
        for disease_a in disease_as:
            one_disease = disease_a.xpath('./text()')[0]
            diseases += str(index) + '.' + one_disease + '\n'
            index += 1

    lock.acquire()
    with open('doctors.csv', 'a', encoding='utf-8_sig') as af:
        writer = csv.writer(af)
        writer.writerow([name, touxian, hospital_name, keshi_name, intro, good_at, diseases])
    lock.release()
    print('页面：{0}爬取成功 一共有：{1}页'.format(url.split('/')[-1], 235000))

    # print(name)
    # print(touxian)
    # print(intro)
    # print(good_at)
    # print(diseases)
    # print(hospital_name)
    # print(keshi_name)


url = 'http://www.cnkang.com/yyk/docindex/{0}/'
pages = 375599


def main():
    with open('doctors.csv', 'w', encoding='utf-8_sig') as af:
        writer = csv.writer(af)
        writer.writerow(['医生姓名', '职称', '出诊医院', '出诊科室', '简介', '擅长疾病', '疾病标签'])

    pool = Pool(20)
    pool.map(yisheng_detail, (url.format(page) for page in range(325000, pages)))


if __name__ == '__main__':
    main()
