# import snscrape
import snscrape.modules
import datetime
import csv
import re
from a import *


# keywords = ['China,border']
# twitter_host = ['timesofindia', 'the_hindu', 'IndianExpress']
keywords = ['China,India']
twitter_host = ['nytimes', 'BBCNewsAsia', 'CNN', 'washingtonpost', 'guardian']

for from_ in twitter_host:
    for keyword in keywords:
        with open('{}.csv'.format(from_), 'w', encoding='utf-8-sig', newline='') as wf:
            csv_writer = csv.writer(wf)
            csv_writer.writerow(['url', 'content', 'date', 'medias', 'retweets', 'favorites', 'comments', 'content_links'])

        with open('{}_comments.csv'.format(from_), 'w', encoding='utf-8-sig', newline='') as wf:
            csv_writer = csv.writer(wf)
            csv_writer.writerow(['user_name', 'content','date', 'favorite', 'content_clean'])
        for tweet in snscrape.modules.twitter.TwitterSearchScraper('{keyword} (from:{from_}) since:{since}'.format(keyword=keyword, from_=from_, since='2020-05-01')).get_items():
            url = tweet.url
            tweet_id = tweet.id
            content = tweet.content
            links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
            if not links:
                links = ''
            date = tweet.date.strftime('%Y-%m-%d %H:%M:%S')
            content = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', content)
            date = tweet.date.strftime('%Y-%m-%d %H:%M:%S')
            medias = tweet.medias
            retweets = tweet.retweetCount
            favorites = tweet.favorite_count
            comments = tweet.reply_count
            print(url, date)


            for item in get_comments(tweet_id):
                item = list(item)
                with open('{}_comments.csv'.format(from_), 'a', encoding='utf-8-sig', newline='') as wf:
                    csv_writer = csv.writer(wf)
                    after = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', item[1])
                    after = re.sub(r'@.*? ', ' ', after)
                    csv_writer.writerow([item[0], item[1], item[2], item[3],after])
            
            with open('{}.csv'.format(from_), 'a', encoding='utf-8-sig', newline='') as wf:
                csv_writer = csv.writer(wf)
                csv_writer.writerow([url, content, date, medias, retweets, favorites, comments, links])
            
