import webbrowser
from weibo import APIClient
import requests
import json
import time

# 在修改后删除这段注释 -------------------------------
# 第一次可能需要手动复制粘贴code值，之后即不用手动操作
# 需要修改的内容
# 1.APP_KEY与APP_SECRET
APP_KEY = ''
APP_SECRET = ''
# 2.自己的Cookie
Cookie = ''
# 3.想自动评论的微博名称
comment_name = ''
# 4.评论内容
comment = ''


def get_code(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Cookie': Cookie,
    }

    url = 'https://api.weibo.com/oauth2/authorize?client_id={0}&response_type=code&redirect_uri=https%3A//api.weibo.com/oauth2/default.html'.format(
        APP_KEY)
    # session = requests.session()
    response = requests.get(url, headers=header, allow_redirects=True)
    with open('r.html', 'w') as wf:
        wf.write(response.text)

    url = response.url
    code = url.split('=')[-1]

    return code


def comment(id):
    r_url = 'https://api.weibo.com/oauth2/default.html'
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=r_url)

    url = client.get_authorize_url()

    try:
        code = get_code(url)
    except:
        webbrowser.open(url)
        code = input('请输入获得的code值：')

    data = {'client_id': APP_KEY,
            'client_secret': APP_SECRET,
            'redirect_uri': r_url,
            'code': code,
            'grant_type': 'authorization_code'}
    result = requests.post(
        url='https://api.weibo.com/oauth2/access_token',
        data=data).json()
    # result = client.request_access_token(code)

    access_token = result['access_token']
    url = 'https://api.weibo.com/2/comments/create.json'
    data = {
        'access_token': access_token,
        'comment': comment,
        'id': '{0}'.format(id)
    }
    response = requests.post(url, data=data)
    print(response.text)


def monitor():
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
    }
    cookie = {
        'Cookie': Cookie
    }
    url = 'https://m.weibo.cn/feed/friends?'
    session = requests.session()
    response = session.get(url, headers=header, cookies=cookie)
    # print(response.text)
    text = json.loads(response.text)
    results = text['data']['statuses']
    for i in results:
        id = i['id']
        screen_name = i['user']['screen_name']
        print(screen_name, id)
        if screen_name == comment_name:  # 填你想自动评论的微博名称
            comment(id)
            pass


if __name__ == '__main__':
    n = 0
    while True:
        monitor()
        time.sleep(30)
        print(n)
        n += 1
