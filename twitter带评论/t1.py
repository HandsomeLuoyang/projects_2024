# import snscrape
import snscrape.modules
import pymongo
import datetime
from analysis import ana

myclient = pymongo.MongoClient("mongodb://localhost:27017/")


while True:
    try:
        mydb = myclient["twitter"]
        mycol = mydb["infos1"]
        st_ed = mydb['st_ed1']

        tm_dict = st_ed.find_one()
        until_time = tm_dict['st']
        since_time = tm_dict['ed']   
        print(since_time, until_time)
        for tweet in snscrape.modules.twitter.TwitterSearchScraper('Chinese until:{} since:{}'.format(until_time, since_time)).get_items():
            username = tweet.username
            content = tweet.content
            date = tweet.date.strftime('%Y-%m-%d %H:%M:%S')
            retweetCount = tweet.retweetCount
            displayName = tweet.username
            followersCount = tweet.followersCount
            location = tweet.userLocation
            sentiment, title = ana(content)
            mycol.insert_one({'username':username, 'content':content, 'date':date, 'retweetCount':retweetCount, 'user_displayname':displayName, 'user_followersCount':followersCount, 'user_location':location, 'sentiment':sentiment, 'title':title})
            print(date, end='\r')
    except KeyboardInterrupt as e:
        # 如果检测到了强制退出，获取现在爬取到了的时间之后的一天
        next_until_date = (datetime.datetime.strptime(date.split()[0], '%Y-%m-%d') + datetime.timedelta(1)).strftime('%Y-%m-%d')

        # 删除爬下来的多余的数据
        # 如果一天的数据都没有爬完，就都不要了
        if next_until_date == until_time:
            result = mycol.delete_many({'date':{'$lt':until_time}})

        else:
            result = mycol.delete_many({'$or':[{'date':{'$lt':next_until_date}, 'date':{'$gt':'2020-01-01'}}]})

        print(result.deleted_count)
        st_ed.update_one(tm_dict, {'$set':{'st':next_until_date}})
        myclient.close()
        exit(0)
    
    except Exception as e:
        print(e)
        next_until_date = (datetime.datetime.strptime(date.split()[0], '%Y-%m-%d') + datetime.timedelta(1)).strftime('%Y-%m-%d')


        if next_until_date == until_time:
            result = mycol.delete_many({'date':{'$lt':until_time}})

        else:
            result = mycol.delete_many({'$or':[{'date':{'$lt':next_until_date}, 'date':{'$gt':'2020-01-01'}}]})

        print(result.deleted_count)
        st_ed.update_one(tm_dict, {'$set':{'st':next_until_date}})

        
    else:
        # 正常爬完
        result = mycol.delete_many({'date':{'$gt':'2020-01-01'}})
        print(result.deleted_count)
        myclient.close()
        exit(0)

