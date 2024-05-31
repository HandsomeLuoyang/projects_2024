# import snscrape
from twitter import TwitterSearchScraper
import datetime
import csv
import re
import json

today = datetime.date.today()
sevens_before = today - datetime.timedelta(7)

str_today = today.strftime('%Y-%m-%d')
str_before = sevens_before.strftime('%Y-%m-%d')

with open('words', 'r') as rf:
    words = rf.readlines()
    for i in range(len(words)-1):
        words[i] = words[i][:-1].strip()
    words = set(words)

# keywords = ['Melbourne', 'Tasmania', 'Sydney', 'Darwin']
keywords = ['Sydney', 'Darwin']

for keyword in keywords:
    with open(f'{keyword}.json', 'w', encoding='utf-8', newline='') as wf:
        wf.write('[\n')

    i = 0
    for tweet in TwitterSearchScraper(f'{keyword} until:{str_today} since:{str_before}').get_items():
        url = tweet.url
        tweet_id = tweet.id
        content = tweet.content
        date = tweet.date.strftime('%Y-%m-%d %H:%M:%S')
        retweets = tweet.retweetCount
        favorites = tweet.favorite_count
        comments = tweet.reply_count
        location = tweet.userLocation
        hashtags = tweet.hashtags
        coordinates = tweet.coordinates
        flag = 0
        zanghua = ''
        for one_word in content.split(' '):
            if one_word in words:
                flag = 1
                zanghua = one_word
                break
                
        if coordinates != '':
            data = {'url': url, 'content': content, 'date': date, 'retweets': retweets, 'favorites': favorites,
                    'comments': comments, 'location': location, 'flag': flag, 'zanghua': zanghua, 'hashtags': hashtags, 'coordinates': coordinates}

            with open(f'{keyword}.json', 'a', encoding='utf-8', newline='') as wf:
                wf.write('\t')
                wf.write(json.dumps(data))
                wf.write(',\n')
            print(url, date, coordinates)
    with open(f'{keyword}.json', 'a', encoding='utf-8', newline='') as wf:
        wf.write(']\n')
