# import snscrape
import snscrape.modules
import datetime
import csv
import re
import requests

# 框架的代理端口在modules的同级目录下base.py里面直接修改即可

# 代理端口测试代码
# r = requests.get(url = 'https://twitter.com/search?f=live&lang=en&q=%28from%3ACGTNOfficial+OR+from%3ASpokespersonCHN%29+until%3A2020-04-30+since%3A2020-01-23&src=spelling_expansion_revert_click', 
#                 proxies = {'http': 'http://localhost:10809', 'https': 'http://localhost:10809'})
# print(r.text)

account_list = ['NBCNewsWorld', 'NBCNews', 'nytimes', 'ChinaDaily', 'CGTNOfficial']


for account in account_list:
    with open("{}.csv".format(account), 'w', newline='', encoding='utf-8-sig') as f:
        csv_write = csv.writer(f)
        csv_head = ['conversationId', 'content','date', 'id', 'lang', 'likeCount',
                    'media', 'mentionedUsers', 'outlinks', 'outlinksss', 'quoteCount',
                    'quotedTweet', 'renderedContent', 'replyCount', 'retweetCount', 'retweetedTweet',
                    'source', 'sourceLabel', 'sourceUrl', 'tcooutlinks', 'tcooutlinksss', 'url', 'user', 'username']
        csv_write.writerow(csv_head)
    for tweet in snscrape.modules.twitter.TwitterSearchScraper("(Xinjiang OR cotton) until:2022-01-06 since:2020-06-01 (from:{})".format(account)).get_items():
        with open("{}.csv".format(account), 'a', newline='', encoding='utf-8-sig') as f:
            print(tweet.username)
            csv_write = csv.writer(f)
            csv_head = [tweet.conversationId, tweet.content,tweet.date.strftime('%Y-%m-%d %H:%M:%S'), tweet.id,
                        tweet.lang, tweet.likeCount, tweet.media, tweet.mentionedUsers,tweet.outlinks,tweet.outlinksss,tweet.quoteCount,
                        tweet.quotedTweet,tweet.renderedContent,tweet.replyCount,tweet.retweetCount,tweet.retweetedTweet,
                        tweet.source,tweet.sourceLabel,tweet.sourceUrl,tweet.tcooutlinks,tweet.tcooutlinksss,tweet.url,tweet.user,tweet.username]
            csv_write.writerow(csv_head)