# -*- coding: UTF-8 -*-
import requests
from lxml import etree
from collections import defaultdict

import csv
import time

# 爬取的是51job招聘网站

# 这里是搜索的关键词
KEYWORD = 'java'

# 这里是数据要保存到的文件夹
SAVA_FILE = 'data1.csv'

# 接下来开始爬取

# 爬取的速度是非常快的


url = 'https://msearch.51job.com/job_list.php?keyword={}&keywordtype=2&funtype=0000&indtype=00&jobarea=000000&workyear=&jobterm=&cotype=&issuedate=9&degree=&saltype=99&cosize=&lonlat=&radius=&landmark=&wxjobid=&filttertype=&pageno={}'
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
}

r = requests.get(url.format(KEYWORD, 1), headers=headers)
html = etree.HTML(r.content.decode('utf8'))
total_pages = int(int(html.xpath('//input[@name="total"]//@value')[0]) // 50 + 1)
print('总页数是{}页面'.format(total_pages))

# 这里是爬取的最大页数, 默认爬取全部
MAX_PAGE = total_pages


def data_crawl():
    for page in range(1, MAX_PAGE+1):
        r = requests.get(url.format(KEYWORD, page), headers=headers)
        text = r.content.decode('utf8')
        html = etree.HTML(text)
        a_list = html.xpath('//*[@id="pageContent"]/div[@class="list"]/a')
        for a in a_list:
            data = defaultdict(str)
            # print(a.xpath('./em/text()'))
            data['job_name'] = a.xpath('./strong/span/text()')
            data['job_salary'] = a.xpath('./i/text()')
            data['job_place'] = a.xpath('./em/text()')
            data['job_info'] = a.xpath('./p/text()')
            data['job_com'] = a.xpath('./aside/text()')
            yield data

    # time.sleep(0.2)


def data_handle():
    with open(SAVA_FILE, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['job_name', 'job_salary',
                    'job_place', 'job_info', 'job_com'])
    for data in data_crawl():
        for key in ['job_name', 'job_salary', 'job_place', 'job_info', 'job_com']:
            if len(data[key]) > 0:
                data[key] = data[key][0]
            else:
                data[key] = ''
        print(data.values())
        with open(SAVA_FILE, 'a', encoding='utf-8-sig', newline='') as f:
            w = csv.writer(f)
            w.writerow(data.values())


def main():
    data_handle()


if __name__ == "__main__":
    main()
