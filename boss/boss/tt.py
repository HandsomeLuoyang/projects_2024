import requests


header = {'jobId': '3dd5841ccfcfd02d1Hx73dm0FlQ~',
        #   'accept': '*/*',
          'accept-encoding': 'gzip, deflate, br',
          'accept-language': 'zh-CN,zh;q=0.9',
          'cookie': 'lastCity=101010100; __c=1582946361; __g=-; _uab_collina=158294636077744405441741; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1582946361; __l=l=https%3A%2F%2Fcn.bing.com%2F&r=https%3A%2F%2Fcn.bing.com%2F&friend_source=0&friend_source=0; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1582967398; __zp_stoken__=2e9c0q4Pu%2FHLJ6yjQ53U%2BeqjqslcmOy7CBAQTyfhhwLrD%2FCbIrvvK8BkHTE6XGngTUBmeFoVrpwuZb6K4mI9CLCD2UENol23YHLWCZaUfhbC5xgSH%2BS89joQwqP1EZO73zFT; __a=68410732.1582946361..1582946361.55.1.55.55; __zp_sname__=775f4cae; __zp_sseed__=eacfhF+utcDzgQf17jNu+BFKxC4QstTodbUwaqe9+S8=; __zp_sts__=1582970787583',
          'referer': 'https://www.zhipin.com/job_detail/3dd5841ccfcfd02d1Hx73dm0FlQ~.html',
          'sec-fetch-dest': 'empty',
          'sec-fetch-mode': 'cors',
          'sec-fetch-site': 'same-origin',
          'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
          'x-requested-with': 'XMLHttpRequest'}


url = 'https://www.zhipin.com/job_detail/3dd5841ccfcfd02d1Hx73dm0FlQ~.html'

proxy = {'https':'https://' + requests.get('http://localhost:5555/random').text}

print(proxy)

response = requests.get(url=url, headers=header, proxies=proxy, timeout=5)
print(response.text)
