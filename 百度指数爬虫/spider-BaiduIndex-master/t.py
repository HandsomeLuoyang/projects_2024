from baidu_index.utils import test_cookies
from baidu_index import config
from baidu_index import BaiduIndex, ExtendedBaiduIndex

cookies = r'BIDUPSID=C7D0E0570022563304CB62205B056C2F; PSTM=1614140102; BAIDUID=C7D0E05700225633010E9BD8E39E3B72:FG=1; BDUSS=U4MUZOV2toZ2MyR3ZUVlBzTGhlOElEa0kzUi1Oa1h2dExpZS1HSFV2T3hpRjFnRVFBQUFBJCQAAAAAAAAAAAEAAADkWyg4uOe1xMP7usWyu9bY0qoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALH7NWCx-zVgRV; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1615350838; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1615350838; bdindexid=e5v8jpmotv5251k9uca1840bp0; RT="z=1&dm=baidu.com&si=ht4twrhbbiu&ss=km2y6iy1&sl=2&tt=2r3&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=34l&ul=5i9"'

if __name__ == "__main__":
    # 测试cookies是否配置正确
    # True为配置成功，False为配置不成功
    print(test_cookies(cookies))

    keywords = [['钟离']]

    # 获取城市代码, 将代码传入area可以获取不同城市的指数, 不传则为全国
    # 媒体指数不能分地区获取
    print(config.PROVINCE_CODE)
    print(config.CITY_CODE)

    # 获取百度搜索指数
    baidu_index = BaiduIndex(
        keywords=keywords,
        start_date='2021-01-01',
        end_date='2021-07-26',
        cookies=cookies
    )
    for index in baidu_index.get_index():
        print(index)
    

    # 获取百度媒体指数
    # news_index = ExtendedBaiduIndex(
    #     keywords=keywords,
    #     start_date='2018-01-01',
    #     end_date='2019-01-01',
    #     cookies=cookies,
    #     kind='news'
    # )
    # for index in news_index.get_index():
    #     print(index)

    # # 获取百度咨询指数
    # feed_index = ExtendedBaiduIndex(
    #     keywords=keywords,
    #     start_date='2018-01-01',
    #     end_date='2019-01-01',
    #     cookies=cookies,
    #     kind='feed'
    # )
    # for index in feed_index.get_index():
    #     print(index)