from time import strftime
import time as tm
import requests
from lxml import etree
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
}


def main():
    list_url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,java,2,{page}.html'
    with open('data.csv', 'a') as af:
        writer = csv.writer(af)
        writer.writerow(['name', 'url', 'salary', 'region', 'cp_name', 'exp', 'edu', 'welfare', 'pubdate', 'detail',
                         'collect_date'])
    # 爬取200页
    for page in range(1, 200):
        r = requests.get(url=list_url, headers=headers)
        print(r.text)
        html = etree.HTML(r.content.decode('gbk'))
        for i in range(4, 54):
            try:
                item = {}
                title = html.xpath('//*[@id="resultList"]/div[{}]/p/span/a/@title'.format(i))
                if title[0] == None:
                    break
                name = html.xpath('//*[@id="resultList"]/div[{}]/span[1]/a/text()'.format(i))
                url = html.xpath('//*[@id="resultList"]/div[{}]/p/span/a/@href'.format(i))
                print(url[0])
                area = html.xpath('//*[@id="resultList"]/div[{}]/span[2]/text()'.format(i))
                salery = html.xpath('//*[@id="resultList"]/div[{}]/span[3]/text()'.format(i))
                time = html.xpath('//*[@id="resultList"]/div[{}]/span[4]/text()'.format(i))
                req1 = requests.get(url[0], headers=headers)
                html1 = etree.HTML(req1.content.decode('gbk'))
                detail = ''.join(html1.xpath('//*[@class="bmsg job_msg inbox"]//*/text()'))
                if detail.isspace():
                    detail = ''.join(html1.xpath('//*[@class="bmsg job_msg inbox"]/text()'))

                region_exp_edu = html1.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/@title')
                region_exp_edu = region_exp_edu[0].split('\xa0\xa0|\xa0\xa0')
                region = region_exp_edu[0]
                cp_name = html1.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[1]/a[1]/@title')
                welfare = '|'.join(html1.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/div/div/span/text()'))

                # 经验、学历、招聘人数、发布日期
                exp = edu = demand = pubdate = skill = ''
                EDU = ['博士', '硕士', '本科', '大专',
                       '中专', '中技', '高中', '初中及以下']
                for i in region_exp_edu:
                    if '经验' in i:
                        exp = i
                    elif i in EDU:
                        edu = i
                    elif '招' in i:
                        demand = i
                    elif '发布' in i:
                        pubdate = i
                    else:
                        skill = i

                item['name'] = title[0]
                item['url'] = url[0]
                item['salary'] = salery[0] if len(salery) != 0 else None
                item['region'] = region
                item['cp_name'] = cp_name[0]
                item['exp'] = exp
                item['edu'] = edu
                item['welfare'] = welfare
                item['pubdate'] = pubdate
                item['detail'] = detail
                item['collect_date'] = strftime('%Y-%m-%d')

                data_list = [v for i, v in item.items()]
                with open('data.csv', 'a') as af:
                    writer = csv.writer(af)
                    writer.writerow(data_list)

            except Exception as e:
                print(e)
                continue
        tm.sleep(1)


if __name__ == '__main__':
    main()
