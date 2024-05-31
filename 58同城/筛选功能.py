import csv
import requests
import json
from math import radians, cos, sin, asin, sqrt


# Haversine(lon1, lat1, lon2, lat2)的参数代表：经度1，纬度1，经度2，纬度2（十进制度数）

def Haversine(lon1, lat1, lon2, lat2):
    """
    获得两个经纬度之间的距离
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # Haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    d = c * r
    print("该两点间距离={0:0.3f} km".format(d))
    # 判断是否小于三十公里
    if d <= 30:
        return True
    else:
        return False


# 接口url
api_url = 'https://restapi.amap.com/v3/geocode/geo'

# 接口参数列表
params = {'key': 'c51a51f65222b18a82f6e0e9e6e60c2d',
          'city': '北京'}


def main():
    # 输入起始地点（即工作地点）
    address = input('请输入位于北京的地址： ')
    # 参数带入
    params['address'] = address
    # 请求接口
    r = requests.get(url=api_url, params=params)
    js = json.loads(r.text)
    # 提取经纬度并转换为float数据类型
    start_jd_location, start_wd_location = js['geocodes'][0]['location'].split(',')
    start_jd_location, start_wd_location = float(start_jd_location), float(start_wd_location)
    # 从csv文件中获取数据进行比对筛选
    with open('new_data.csv', 'r', encoding='utf-8_sig') as rf:
        reader = csv.reader(rf)
        # 跳过csv文件头
        reader.__next__()

        lst = []
        # 循环遍历所有的房源信息
        for item in reader:
            end_jd_location, end_wd_location = float(item[4]), float(item[5])
            # 进行比对，比对成功就打印信息
            if Haversine(start_jd_location, start_wd_location,
                         end_jd_location, end_wd_location):
                print(item[0], item[1], item[3])
                lst.append([item[0], item[1], item[2], item[3].split()[0]])
        while True:
            opt = input('是否根据价格继续筛选?(y/n)')
            if opt == 'y':
                start_price = int(input('请输入最低价格：'))
                end_price = int(input('请输入最高价格：'))
                for i in lst:
                    if float(i[3]) > start_price and float(i[3]) < end_price:
                        print('【' + '  '.join(i) + '元/月 】')
            else:
                break


if __name__ == '__main__':
    main()
    # Haversine(111.474723, 27.216472, 112.169608, 27.255545)
