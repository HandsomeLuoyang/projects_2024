from os import write
import requests
import json
from urllib.parse import quote
import pandas as pd
import csv

##
"""
通过推文的id来爬取所有的转推人的昵称
"""

##
# print(quote(varss, encoding='utf-8'))

# varss = 'variables={"tweetId":"1481116331680440324","count":20,"cursor":"HBaAgID0rOzm5C8AAA==","withTweetQuoteCount":false,"includePromotedContent":true,"withSuperFollowsUserFields":true,"withBirdwatchPivots":false,"withDownvotePerspective":false,"withReactionsMetadata":false,"withReactionsPerspective":false,"withSuperFollowsTweetFields":true}'

# 请求头
headers = {
    'x-csrf-token': 'ad1bb14be75924d1e48465ba93bb0865330bfdf7a81856c16147a9ce26d2b002f1e8c09666ae4fd2d1b1682abd302fcc69e9913b8296a50875cf4d55d77ca31030bac8b8ad345b3ca64094521a4795db',
    'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    'Cookie': 'kdt=IuRA1MDbTMf4ZEiGvhQiviWH2lu67KMf68wOqKJ7; remember_checked_on=1; des_opt_in=Y; guest_id=v1%3A162815010810678773; G_ENABLED_IDPS=google; auth_token=f92e147d33abeb2b2e05cbab014877085e22f804; ct0=ad1bb14be75924d1e48465ba93bb0865330bfdf7a81856c16147a9ce26d2b002f1e8c09666ae4fd2d1b1682abd302fcc69e9913b8296a50875cf4d55d77ca31030bac8b8ad345b3ca64094521a4795db; twid=u%3D1423205471599534084; guest_id_marketing=v1%3A162815010810678773; guest_id_ads=v1%3A162815010810678773; personalization_id="v1_1y+z3CgxfyV0eqRVbz+q3Q=="; _gid=GA1.2.1621865468.1641903688; at_check=true; lang=zh-cn; _gcl_au=1.1.143258453.1641905899; mbox=session#902894c15b9f4420a27b0340ec36010c#1641909772|PC#902894c15b9f4420a27b0340ec36010c.38_0#1705152712; _ga=GA1.2.1595148897.1639454710; _ga_34PHSZMC42=GS1.1.1641914261.2.0.1641914261.0',
}

df = pd.read_csv('data2.csv')
with open('retweet.csv', 'a', encoding='utf-8-sig', newline='') as af:
    writer = csv.writer(af)
    writer.writerow(['host', 'ret_name'])
    for ids in df['id']:
    # 首次的参数，其中tweetId要根据不同推文调整
        varss = '{{"tweetId":"{id}","count":20,"withTweetQuoteCount":false,"includePromotedContent":true,"withSuperFollowsUserFields":true,"withBirdwatchPivots":false,"withDownvotePerspective":false,"withReactionsMetadata":false,"withReactionsPerspective":false,"withSuperFollowsTweetFields":true}}'.format(id=ids)
        varss2 = '{{"tweetId":"{id}","cursor":"%s","count":20,"withTweetQuoteCount":false,"includePromotedContent":true,"withSuperFollowsUserFields":true,"withBirdwatchPivots":false,"withDownvotePerspective":false,"withReactionsMetadata":false,"withReactionsPerspective":false,"withSuperFollowsTweetFields":true}}'.format(id=ids)
        while True:
            try:
                r = requests.get('https://twitter.com/i/api/graphql/7NhBVRkuN3bsCiIUU2VQCw/Retweeters?variables={}'.format(quote(varss, encoding='utf-8')),
                                proxies = {'http': 'http://localhost:10809', 'https': 'http://localhost:10809'},
                                headers=headers)
            except:
                continue
            else:
                break
        print(r.status_code)
        print(ids)
        js = json.loads(r.text)

        entries = js['data']['retweeters_timeline']['timeline']['instructions'][0]['entries']
        value = entries[-1]['content']['value']

        while True:
            if len(entries) <= 2 or r.status_code!=200:
                print(r.text)
                break
            
            for entry in entries[:-2]:
                try:
                    ret_name = entry['content']['itemContent']['user_results']['result']['legacy']['screen_name']
                    writer.writerow([ids, ret_name])
                except:
                    pass

            print(value)
            print(len(entries))
            varss = varss2 % value
            while True:
                try:
                    r = requests.get('https://twitter.com/i/api/graphql/7NhBVRkuN3bsCiIUU2VQCw/Retweeters?variables={}'.format(quote(varss, encoding='utf-8')),
                                proxies = {'http': 'http://localhost:10809', 'https': 'http://localhost:10809'},
                                headers=headers)
                except:
                    continue
                else:
                    break
            print(r.status_code)
            js = json.loads(r.text)
            entries = js['data']['retweeters_timeline']['timeline']['instructions'][0]['entries']
            value = entries[-1]['content']['value']