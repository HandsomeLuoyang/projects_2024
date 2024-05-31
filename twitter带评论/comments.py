import csv
from a import *
import re

lst = ['IndianExpress', 'nytimes', 'BBCNewsAsia', 'CNN', 'washingtonpost', 'guardian']


for file in lst:
    with open(file+'.csv', 'r', encoding='utf8') as rf:
        print('open file: ' + file)
        csv_rf = csv.reader(rf)
        index = 0
        with open('{}_comments.csv'.format(file), 'w', encoding='utf-8-sig', newline='') as wf:
            csv_writer = csv.writer(wf)
            csv_writer.writerow(['user_name', 'content','date', 'favorite', 'content_clean'])
        for i in csv_rf:
            if index == 0:
                index += 1
                continue
            tweet_id = i[0].split('/')[-1]
            print("index: " + str(index))
            print("url: " + i[0])
            print("comment_count: " + i[6])
            print("time: " + i[2])
            index += 1
            for item in get_comments(tweet_id):
                item = list(item)
                with open('{}_comments.csv'.format(file), 'a', encoding='utf-8-sig', newline='') as wf:
                    csv_writer = csv.writer(wf)
                    after = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', item[1])
                    after = re.sub(r'@.*? ', ' ', after)
                    try:
                        print('comment: ' + after)
                    except:
                        pass
                    csv_writer.writerow([item[0], item[1], item[2], item[3],after])
            print(' ')
