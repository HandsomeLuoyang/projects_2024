import requests
import time
import csv
from lxml import etree
from fontTools.ttLib import TTFont
from io import BytesIO
import re
import base64

# 定义列表页网址，设置翻页格式化参数
list_url = 'https://bj.58.com/wangjing/chuzu/pn{0}/?PGTID=0d3090a7-004b-30bc-9cc5-34e91af08390&ClickID=2'


# 定义请求头
# 设置UA（user-agent)避免被认出是爬虫
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
}

# 定义请求页数
pages = 70


def handlefont(page_source):
    """css加密字体处理函数"""
    # 利用正则表达式提取base64加密字符串
    base64_str = re.search(r"charset=utf-8;base64,(.*?)'\)",page_source).group(1)

    # 将加密后的字符串揭秘之后转换为TTFont对象
    font = TTFont(BytesIO(base64.decodebytes(base64_str.encode())))

    # 从TTFont对象中提取映射关系
    first_dict = font['cmap'].getBestCmap()

    # 处理映射关系
    second_dict = {}
    for k, v in first_dict.items():
        second_dict['&#' + hex(k)[1:] + ';'] = int(v[-2:]) - 1

    # 利用映射关系进行替换
    for k, v in second_dict.items():
        if k in page_source:
            page_source = page_source.replace(k, str(v))

    # 返回处理之后的页面
    return page_source


def main():
    # 写入csv文件头
    with open('data.csv', 'w', encoding='utf-8_sig', newline='') as wf:
        writer = csv.writer(wf)
        writer.writerow(['标题', '详情链接', '地址', '价格'])

    # 循环爬取每一页
    for page in range(1, pages):
        # 打印当前页面
        print('当前页面：{}'.format(page))

        while True:
            # 发送get请求，获取页面信息
            # 若是碰到验证码信息，请手动进入浏览器验证过关，过关后程序会继续
            r = requests.get(url=list_url.format(page), headers=headers)
            if '访问过于频繁，本次访问做以下验证码校验。' not in r.text:
                break
            print('碰到验证！请点击下方链接前往验证：')
            print(list_url.format(page))

            time.sleep(2)

        # 将返回回来的文档进行css破解替换，然后再进入到网页元素提取
        real_text = handlefont(r.text)

        # 生成etree树，以便分析页面元素，提取需要信息
        html = etree.HTML(real_text)

        # 分析网页结构
        # 列表
        house_lis = html.xpath('//li[@class="house-cell"]')
        if house_lis:
            for house_li in house_lis:
                # 从列表li中获取房源名称
                name = house_li.xpath(
                    './div[@class="des"]/h2/a/text()')[0].strip()
                # 同理获取详情链接
                detail_url = house_li.xpath(
                    './div[@class="des"]/h2/a/@href')[0]
                # 获取地址
                address = ' '.join(''.join(house_li.xpath(
                    './div[@class="des"]/p[@class="infor"]//text()')).split())
                # 获取价格
                price = ' '.join(house_li.xpath(
                    './/div[@class="money"]//text()')[-2:])

                # 将获取到的信息存储到csv文件当中
                with open('data.csv', 'a', encoding='utf-8_sig', newline='') as wf:
                    writer = csv.writer(wf)
                    writer.writerow([name, detail_url, address, price])

        time.sleep(2)


if __name__ == '__main__':
    main()
