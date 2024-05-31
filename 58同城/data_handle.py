# coding:utf-8
import requests
import json
import csv
import time

# 这个py文件用于从高德api获取当前房源地址的经纬度并和原来的信息一起存入一个新的csv文件当中

# api接口
api_url = 'https://restapi.amap.com/v3/geocode/geo'

# 接口参数
params = {'key': 'c51a51f65222b18a82f6e0e9e6e60c2d',
          'city': '北京'}


def get_loaction():
    """
    调用高德api接口从地址获取经纬度并存储
    """
    # 打开原来的csv文件
    with open('data.csv', 'r', encoding='utf-8_sig') as rf:
        # 创建csv阅读对象
        reader = csv.reader(rf)
        # 跳过第一行，因为第一行是csv文件头
        reader.__next__()
        with open('new_data.csv', 'a', encoding='utf-8_sig', newline='') as af:
            writer = csv.writer(af)
            # 写入新csv文件的文件头
            writer.writerow(['标题', '详情链接', '地址', '价格', '经度', '纬度'])
            for item in reader:
                # 获取详细地址
                try:
                    address = item[2].split()[0] + item[2].split()[1]
                except Exception as ret:
                    print(ret)
                    print(item[2])
                # 加入到参数里面去
                params['address'] = address
                # 调用接口
                r = requests.get(url=api_url, params=params)
                # json加载
                js = json.loads(r.text)
                # 获得经纬度
                jd_location, wd_location = js['geocodes'][0]['location'].split(',')
                print(jd_location, wd_location)
                # 存储
                writer.writerow([item[0], item[1], item[2], item[3], jd_location, wd_location])
                # 高德接口并发每秒五次，所以每请求一次停止0.2秒
                time.sleep(0.2)


if __name__ == '__main__':
    get_loaction()
