import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import datetime

city_locations = {
    'Melbourne': [144.668792, -38.312755, 145.378509, -37.705070],
    'Tasmania': [147.175928, -43.082853, 147.674799, -42.598515],
    'Sydney': [150.902511, -34.007028, 151.316184, -33.644015],
    'Darwin': [130.825607, -12.467706, 130.935127, -12.371143]
}

city = 'Melbourne'

with open('words', 'r') as rf:
    words = rf.readlines()
    for i in range(len(words)-1):
        words[i] = words[i][:-1].strip()
    words = set(words)

class StdOutListener(StreamListener):
    def __init__(self):
        with open(f'stream_{city}.json', 'w', encoding='utf-8', newline='') as wf:
            wf.write('[\n')

    def on_data(self, data):
        print(data)
        data = json.loads(data)
        content = data['text']
        # date = data['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        date = str(datetime.datetime.strptime(
                            data['created_at'], '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=datetime.timezone.utc))
        place = data['place']['full_name']
        coordinates = str(data['place']['bounding_box']['coordinates'])
        hashtags = str(data['entities']['hashtags'])

        flag = 0
        zanghua = ''
        for one_word in content.split(' '):
            if one_word in words:
                flag = 1
                zanghua = one_word
                break

        handle_data = {'content':content, 'date':date, 'place':place, 'coordinates':coordinates, 'hashtags':hashtags, 'flag':flag, 'zanghua':zanghua}
        with open(f'stream_{city}.json', 'a', encoding='utf-8', newline='') as wf:
                wf.write('\t')
                wf.write(json.dumps(handle_data))
                wf.write(',\n')
        return True

    def on_error(self, status):
        print(status)
        if status == 420:
            return False


class TwitterStreamer():
    def __init__(self):
        pass

    def stream_tweets(self):
        listener = StdOutListener()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, listener)

        stream.filter(locations=city_locations[f'{city}'], languages=['en'])

#####################################################################################


#####################################################################################
if __name__ == "__main__":
    # Twitter API Credentials
    consumer_key = "XmVsJRVkjlIq2GBIR65cW3efB"  # write consumer key here
    # write consumer secret here
    consumer_secret = "32RXvo6v49UU5ixL5bcWi8TOAa1chWgsyA5ROdwKiLnbmg80ZY"
    # write access_token here
    access_token = "1385175482149208068-blZFS8ame8qtcNqxFB851YP64FgHaq"
    # write access token secret here
    access_token_secret = "5mw7Q6V7WklVHL8ZBIDOyDsLDYn114rkto1FLkjMxNRiK"

    # Search Area: Australia
    # locations = city_locations['Darwin']

    # Keywords for Search in Twitter: A list of strings
    # keywords=['study','education','homeschooling','school','homework','assignment']

    twitter_streamer = TwitterStreamer()

    # (Server, Database Name, Keywords)
    twitter_streamer.stream_tweets()
