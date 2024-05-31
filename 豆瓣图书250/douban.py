import requests
from lxml import etree
import sqlite3
from openpyxl import Workbook

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    # 'Accept-Encoding': 'gzip, deflate, br',
    # 'Cookie': 'bid=nUBoe4XdxSU',
}

base_url = 'https://book.douban.com/top250?start={}'


def main():
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    book = Workbook()
    sheet = book.active

    sheet['A1'] = 'name'
    sheet['B1'] = 'c_na'
    sheet['C1'] = 'pub_time'
    sheet['D1'] = 'price'
    sheet['E1'] = 'score'
    sheet['F1'] = 'comment_num'

    index = 2
    for i in range(0, 226, 25):
        r = requests.get(url=base_url.format(i), headers=headers)
        print(r.url)
        html = etree.HTML(r.text)
        tables = html.xpath('//*[@id="content"]/div/div[1]/div/table')
        for table in tables:
            # 书名
            name = table.xpath('./tr/td[2]/div/a/text()')[0].strip()

            infos = table.xpath('./tr/td[2]/p[1]/text()')[0].split('/')

            # 国籍与作者名字
            c_na = infos[0].strip()
            # 出版时间
            pub_time = infos[-2].strip()
            # 价格
            price = infos[-1].strip()

            # 评分
            score = table.xpath('./tr/td[2]/div[2]/span[2]/text()')[0].strip()
            # 评价人数
            comment_num = table.xpath(
                './tr/td[2]/div[2]/span[3]/text()')[0].strip()
            comment_num = comment_num[1:-1].strip()

            print(name)

            cursor.execute('insert into data(name, c_na, pub_time, price, score, comment_num) values ("%s", "%s", "%s", "%s", "%s", "%s")' % (
                name, c_na, pub_time, price, score, comment_num))
            conn.commit()
            sheet['A{}'.format(index)] = name
            sheet['B{}'.format(index)] = c_na
            sheet['C{}'.format(index)] = pub_time
            sheet['D{}'.format(index)] = price
            sheet['E{}'.format(index)] = score
            sheet['F{}'.format(index)] = comment_num
            index += 1

    book.save('data.xlsx')
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
