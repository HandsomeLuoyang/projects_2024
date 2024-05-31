import tweepy
import csv
import datetime
import json

# Twitter API Credentials
consumer_key = "RLLbDhlYOobzDcIVuyxHjPMha"  # write consumer key here
# write consumer secret here
consumer_secret = "bi2E4x5LP3GFFuFTNZY6BBeT6gAjhrJtrSghjxAFDJaUGxOgZT"
# write access_token here
access_token = "1385175482149208068-TSVcfCt8y1Sld4evz2iaTkGB2PanVF"
# write access token secret here
access_token_secret = "WaEuYjHqa0Z7m1Pw6rN0CBRPtbCgZMPTTRSnED5nCHIyx"

auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

city_locations = {
    'Melbourne': [144.668792, -38.312755],
    'Tasmania': [147.175928, -43.082853],
    'Sydney': [150.902511, -34.007028],
    'Darwin': [130.825607, -12.467706]
}

CITY = 'Melbourne'

today = datetime.date.today()
sevens_before = today - datetime.timedelta(7)

str_today = today.strftime('%Y-%m-%d')
str_before = sevens_before.strftime('%Y-%m-%d')

with open('words', 'r') as rf:
    words = rf.readlines()
    for i in range(len(words)-1):
        words[i] = words[i][:-1].strip()
    words = set(words)

with open(f'{CITY}.json', 'w', encoding='utf-8', newline='') as wf:
            wf.write('[\n')

for tweet in tweepy.Cursor(api.search, q=f"until:{str_today} since:{str_before} lang:en", geocode=f"{city_locations[CITY][1]},{city_locations[CITY][0]},100km").items():
    # print([tweet.created_at, tweet.text.encode('utf-8'), tweet.user.id, tweet.geo])
    # print(tweet._json)
    data = tweet._json
    content = data['text']
    # date = data['created_at'].strftime('%Y-%m-%d %H:%M:%S')
    date = str(datetime.datetime.strptime(
        data['created_at'], '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=datetime.timezone.utc))

    try:
        place = data['place']['full_name']
    except Exception as e:
        # print(e)
        continue
    coordinates = str(data['place']['bounding_box']['coordinates'])
    hashtags = [item['text'] for item in data['entities']['hashtags']]

    flag = 0
    zanghua = ''
    for one_word in content.split(' '):
        if one_word in words:
            flag = 1
            zanghua = one_word
            break

    handle_data = {'content': content, 'date': date, 'place': place,
                   'coordinates': coordinates, 'hashtags': hashtags, 'flag': flag, 'zanghua': zanghua}
    print(date, place, hashtags, flag, zanghua)
    with open(f'{CITY}.json', 'a', encoding='utf-8', newline='') as wf:
        wf.write('\t')
        wf.write(json.dumps(handle_data))
        wf.write(',\n')