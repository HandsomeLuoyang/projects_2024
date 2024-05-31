import requests
import snscrape.base
import typing
import datetime
import time
import snscrape.base
import json
headers = {
    'x-csrf-token': 'd126d60b63a1b96a56fef521f41fa386b4a6ebc447094db0e29b91abdc671e838e95275b08ab2c1369c926a76748140712036e5cbf0d87b9df8873febf199d57e50a6e6268afa3b8fe8ff24572d72de3',
    'cookie': 'kdt=clwkfwTrzONp2ib1LNIhvCVzR8siVK5OxdMgUeNF; dnt=1; remember_checked_on=1; _ga=GA1.2.1929021451.1596688736; des_opt_in=Y; personalization_id="v1_0gIsCh+UHBeGISjEZkFOxg=="; guest_id=v1%3A160021774562584028; auth_token=dad77134a6a4422af8b56a9761bed73920b222f5; twid=u%3D1306546630838026240; ct0=d126d60b63a1b96a56fef521f41fa386b4a6ebc447094db0e29b91abdc671e838e95275b08ab2c1369c926a76748140712036e5cbf0d87b9df8873febf199d57e50a6e6268afa3b8fe8ff24572d72de3; lang=zh-cn; external_referer=padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0|8e8t2xd8A2w%3D',
    'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
}

params = {
    'include_profile_interstitial_type': '1',
    'include_blocking': '1',
    'include_blocked_by': '1',
    'include_followed_by': '1',
    'include_want_retweets': '1',
    'include_mute_edge': '1',
    'include_can_dm': '1',
    'include_can_media_tag': '1',
    'skip_status': '1',
    'cards_platform': 'Web-12',
    'include_cards': '1',
    'include_composer_source': 'true',
    'include_ext_alt_text': 'true',
    'include_reply_count': '1',
    'tweet_mode': 'extended',
    'include_entities': 'true',
    'include_user_entities': 'true',
    'include_ext_media_color': 'true',
    'include_ext_media_availability': 'true',
    'send_error_codes': 'true',
    'simple_quoted_tweets': 'true',
    'count': '20',
    'include_ext_has_birdwatch_notes': 'false',
    'ext': 'mediaStats,highlightedLabel',
}


class Tweet(typing.NamedTuple, snscrape.base.Item):
    url: str
    date: datetime.datetime
    content: str
    id: int
    username: str
    outlinks: list
    outlinksss: str
    tcooutlinks: list
    tcooutlinksss: str
    retweetCount: int
    displayName: str
    followersCount: int
    userLocation: str
    medias: list
    favorite_count: int
    reply_count: int

    def __str__(self):
        return self.url



def get_comments(tweet_id):
    base_url = 'https://twitter.com/i/api/2/timeline/conversation/{tweet_id}.json'
    cursor = None   
    while True:
        if cursor:
            params['cursor'] = cursor
        else:
            if 'cursor' in params.keys():
                params.pop('cursor')
        while True:
            try:
                r = requests.get(url=base_url.format(
                        tweet_id=tweet_id), headers=headers, params=params, timeout=1)
            except Exception as e:
                print(e)
            else:
                break
        obj = r.json()
        with open('t.json', 'w', encoding='utf8') as wf:
            json.dump(obj, wf)

        newCursor = None
        try:
            tweets = obj['globalObjects']['tweets']
        except:
            newCursor = None
            continue
        for tweet_key in tweets.keys():
            if tweet_key == tweet_id:
                continue
            user_id = tweets[tweet_key]['user_id_str']
            reply_time = datetime.datetime.strptime(tweets[tweet_key]['created_at'], '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo = datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            user_name = obj['globalObjects']['users'][user_id]['screen_name']
            content = tweets[tweet_key]['full_text']
            favorite = tweets[tweet_key]['favorite_count']
            yield (user_name, content, reply_time, favorite)
        try:
            newCursor = obj['timeline']['instructions'][0]['addEntries']['entries'][-1]['content']['operation']['cursor']['value']
        except Exception as e:
            newCursor = None
        if not newCursor or newCursor == cursor:
            break
        cursor = newCursor
