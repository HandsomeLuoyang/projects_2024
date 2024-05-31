# coding:utf-8
import requests
from lxml import etree
import threading
import time
import csv
import random
import traceback
import re

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

dept_url = 'http://www.cnkang.com/yyk/hospdept/{0}/'
intro_url = 'http://www.cnkang.com/yyk/hospintro/{0}/'

host_url = 'http://www.cnkang.com{0}'


def yisheng_detail(hospital_name, keshi_name, url):
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
            good_at = html.xpath('//ul[@class="ys10a"][2]/text()')[0].strip()
            disease_as = html.xpath('//div[@class="ys10b"]/ul/a')
        except Exception as ret:
            # traceback.print_exc()
            # print(url)
            # print(r.status_code)
            with open('r.html', 'w') as wf:
                wf.write(r.text)
        else:
            try:
                intro = html.xpath('//ul[@class="ys10a"][1]/div/text()')[0].strip()
            except Exception as ret:
                intro = '暂无信息'
            break

    diseases = ''
    index = 1

    for disease_a in disease_as:
        one_disease = disease_a.xpath('./text()')[0]
        diseases += str(index) + '.' + one_disease + '\n'
        index += 1

    lock.acquire()
    with open('doctors.csv', 'a', encoding='utf-8_sig') as af:
        writer = csv.writer(af)
        writer.writerow([name, touxian, hospital_name, keshi_name, intro, good_at, diseases])
    lock.release()
    # print(name)
    # print(touxian)
    # print(intro)
    # print(good_at)
    # print(diseases)


def yisheng_list(hospital_name, keshi_name, url):
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
            divs = html.xpath('//div[@class="main_content"]/div/div')
            for div in divs:
                doc_url = host_url.format(div.xpath('./a/@href')[0])
                t = threading.Thread(target=yisheng_detail, args=(hospital_name, keshi_name, doc_url))
                t.start()
                time.sleep(3)
        except:
            traceback.print_exc()
        else:
            break


def chanke_detail(hospital_name, father_name, son_name, url):
    try:
        headers['User-Agent'] = random.choice(ua_list)
        while True:
            r = requests.get(url=url, headers=headers)
            if r.status_code == 200:
                break
            try:
                headers['User-Agent'] = random.choice(ua_list)
                r = requests.get(url=url, headers=headers, proxies=proxies, timeout=2)
                time.sleep(1)
            except:
                pass
            else:
                break

        html = etree.HTML(r.text)
        intro = ''.join(html.xpath('//div[@class="ys12g"]/p[2]/text()')).strip()
        disease_uls = html.xpath('//div[@class="ys13b1"]/ul')
    except Exception as ret:
        traceback.print_exc()
        print(url)

    all_disease = ''
    index = 1
    for disease_ul in disease_uls:
        disease_name = disease_ul.xpath('./a/text()')[0]
        disease_url = host_url.format(disease_ul.xpath('./a/@href')[0])

        all_disease += str(index) + '.' + disease_name + '\n'
        index += 1

        # t = threading.Thread(target=yisheng_list, args=(hospital_name, son_name, disease_url))
        #
        # t.start()
        # time.sleep(1)

    lock.acquire()
    with open('keshi.csv', 'a', encoding='utf-8_sig') as af:
        writer = csv.writer(af)
        writer.writerow([hospital_name, father_name, son_name, intro, all_disease])
    lock.release()

    # print(hospital_name)
    # print(father_name)
    # print(son_name)
    # print(intro)
    # print(all_disease)


# 5143
def get_hospital_detail():
    for i in range(3258, 3500):
        print('当前页面：{0}   最终页面:{1}'.format(i, 5143))
        while True:
            flag = 0
            try:
                headers['User-Agent'] = random.choice(ua_list)
                while True:
                    res = requests.get(url=dept_url.format(i), headers=headers)
                    if res.status_code == 200:
                        break
                    try:
                        res = requests.get(url=dept_url.format(i), headers=headers, proxies=proxies, verify=False)
                        time.sleep(2)
                    except:
                        pass
                    else:
                        break
                if res.status_code == 404:
                    flag = 1

                headers['User-Agent'] = random.choice(ua_list)
                while True:
                    res2 = requests.get(intro_url.format(i), headers)
                    if res2.status_code == 200:
                        break
                    try:
                        res2 = requests.get(url=intro_url.format(i), headers=headers, proxies=proxies)
                        time.sleep(1)
                    except:
                        pass
                    else:
                        break

                html = etree.HTML(res.text)
                hostpital_name = html.xpath('//div[@class="ys11_name"]/ul/text()')[0].strip()
                # 获取大分类标签div
                divs = html.xpath('//div[@class="yslist06 yslist06b"]/div')

                html_2 = etree.HTML(res2.text)

                hospital_level = html_2.xpath('//div[@class="ys11_name"]/p/text()')
                if not hospital_level:
                    hospital_level = '无'
                else:
                    hospital_level = hospital_level[0].strip()

                info_ul_list = html_2.xpath('//ul[@class="ys11_jx"]/li')

                hospital_spcial = '无'
                hospital_phone = '无'
                hospital_address = '无'

                for li in info_ul_list:
                    span = li.xpath('./span/text()')[0].strip()
                    if '特色' in span:
                        hospital_spcial = li.xpath('./text()')[0].strip()
                    elif '电话' in span:
                        hospital_phone = li.xpath('./text()')[0].strip()
                    elif '地址' in span:
                        hospital_address = li.xpath('./text()')[0].strip()
                    else:
                        pass
                hospital_content = ''.join(html_2.xpath('//div[@class="ys12a"]/p/text()')).strip()

            except Exception as ret:
                if flag == 1:
                    break
                traceback.print_exc()
                print(dept_url.format(i))
                print(intro_url.format(i))
                print(res.status_code)
            else:
                break
        if flag == 1:
            continue

        all_keshi = ''
        keshi_index = 1
        for div in divs:
            try:
                # 大分类名称
                big_class_name = div.xpath('./ol/a/text()')[0].strip()
                # 在大分类中获取小分类list，获取小分类的URL和名称
                little_class_list = div.xpath('./ul/li')
                for li in little_class_list:
                    li_url = host_url.format(li.xpath("./a/@href")[0])
                    li_name = li.xpath("./a/text()")[0].strip()
                    all_keshi += str(keshi_index) + '.' + li_name + '\n'
                    keshi_index += 1
                    t = threading.Thread(target=chanke_detail, args=(hostpital_name,
                                                                     big_class_name,
                                                                     li_name, li_url))
                    t.start()
            except:
                pass

        with open('histopital.csv', 'a', encoding='utf-8_sig') as af:
            writer = csv.writer(af)
            writer.writerow([hostpital_name, hospital_level, hospital_spcial,
                             hospital_phone, hospital_address, hospital_content, all_keshi])
        time.sleep(1.5)


def main():
    # with open('histopital.csv', 'w', encoding='utf-8_sig') as af:
    #     writer = csv.writer(af)
    #     writer.writerow(['医院名称', '等级', '特色', '电话', '地址', '简介', '科室列表'])
    # with open('keshi.csv', 'w', encoding='utf-8_sig') as af:
    #     writer = csv.writer(af)
    #     writer.writerow(['医院名称', '所属父科', '子科室名称', '介绍', '疾病'])
    # with open('doctors.csv', 'w', encoding='utf-8_sig') as af:
    #     writer = csv.writer(af)
    #     writer.writerow(['医生姓名', '职称', '出诊医院', '出诊科室', '简介', '擅长疾病', '疾病标签'])

    get_hospital_detail()


if __name__ == '__main__':
    main()
