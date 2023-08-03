import tweepy
from dotenv import load_dotenv
import os

from tweepy import TweepyException


def get_api():
    load_dotenv()  # take environment variables from .env.
    auth = tweepy.OAuth2BearerHandler(
        bearer_token=os.environ['BEARER'])
    return tweepy.API(auth, wait_on_rate_limit=True)


def search_tweets(q, api, **search_args):
    done = False
    while not done:
        try:
            for page in tweepy.Cursor(api.search_tweets, q=q, **search_args).pages():
                yield from page
                if (page is None) or not len(page):
                    done = True
                    break
        except TweepyException as e:
            print(e)


if __name__ == '__main__':

    api = get_api()
    for tweet in search_tweets(
            q='lang:en -filter:retweets -filter:replies '
              '(card_name:poll2choice_text_only OR '
              'card_name:poll2choice_text_only OR '
              'card_name:poll3choice_text_only OR '
              'card_name:poll4choice_text_only OR '
              'card_name:poll2choice_image OR '
              'card_name:poll3choice_image OR '
              'card_name:poll4choice_image)',
            api=api, count=180):
        print(f'{tweet._json["id"]} {tweet._json["text"]}')
