import requests
from lxml import etree
from openpyxl import Workbook
import time

book = Workbook()
sheet = book.active
sheet['A1'] = '机构编码'
sheet['B1'] = '机构名称'
sheet['C1'] = '批准成立日期'
sheet['D1'] = '发证日期'
sheet['E1'] = '机构地址'
sheet['F1'] = '机构所在地'
sheet['G1'] = '机构简称'
sheet['H1'] = '发证机关'
sheet['I1'] = '流水号'
sheet['J1'] = '退出时间'


base_url = 'http://xkz.cbirc.gov.cn/jr/getLicence.do?useState=7'
detail_url = 'http://xkz.cbirc.gov.cn/jr/showLicenceInfo.do?id={}'

proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"
proxyUser = "H81N31II078KW84D"
proxyPass = "B2DD71DC314F9DE3"
proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}


data = {
    'start': 0,
    'limit': 10,
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
}


def get_detail(url, jianyan):
    while True:
        try:
            r = requests.get(url, proxies=proxies, headers=headers, timeout=1)
            assert jianyan in r.text
        except Exception as e:
            print(e)
            time.sleep(0.1)
        else:
            if r.status_code == 200:
                break
    html = etree.HTML(r.text)
    trs = html.xpath('/html/body/div[2]/table/tr')
    address = ''
    at = ''
    brief = ''
    insti = ''
    _id = ''
    out_time = ''
    for tr in trs:
        if '机构地址' in ''.join(tr.xpath('.//text()')):
            address = tr.xpath('./td[2]/text()')[0]
        if '机构所在地' in ''.join(tr.xpath('.//text()')):
            at = tr.xpath('./td[2]/text()')[0]
        if '机构简称' in ''.join(tr.xpath('.//text()')):
            brief = tr.xpath('./td[2]/text()')[0]
        if '发证机关' in ''.join(tr.xpath('.//text()')):
            insti = tr.xpath('./td[2]/text()')[0]
        if '流水号' in ''.join(tr.xpath('.//text()')):
            _id = tr.xpath('./td[2]/text()')[0]
        if '退出时间' in ''.join(tr.xpath('.//text()')):
            out_time = tr.xpath('./td[2]/text()')[0]
    if not insti or not _id:
        print(r.url)
        print(r.text)
    return address.strip(), at.strip(), brief.strip(), insti.strip(), _id.strip(), out_time.strip()


index = 2
for item in range(0, 7211, 10):
    print('起始值:{}'.format(item))
    data['start'] = item
    datas = []
    while True:
        time.sleep(0.1)
        try:
            r = requests.post(url=base_url, data=data, proxies=proxies, headers=headers, timeout=1)
            datas = r.json()['datas']
        except Exception as e:
            print(e)
            print('列表页爬取异常')
            continue
        else:
            if len(datas) != 0:
                break
            else:
                print(r.json())

    for one_data in datas:
        certCode = one_data['certCode']
        fullName = one_data['fullName']
        setDate = one_data['setDate']
        printDate = one_data['printDate']
        lst = [certCode, fullName, setDate, printDate]
        lst.extend(get_detail(detail_url.format(one_data['id']), fullName))
        sheet['A{}'.format(index)] = lst[0]
        sheet['B{}'.format(index)] = lst[1]
        sheet['C{}'.format(index)] = lst[2]
        sheet['D{}'.format(index)] = lst[3]
        sheet['E{}'.format(index)] = lst[4]
        sheet['F{}'.format(index)] = lst[5]
        sheet['G{}'.format(index)] = lst[6]
        sheet['H{}'.format(index)] = lst[7]
        sheet['I{}'.format(index)] = lst[8]
        sheet['J{}'.format(index)] = lst[9]
        index += 1
        print(lst)

book.save('机构退出列表.xlsx')
