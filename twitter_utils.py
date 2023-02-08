import json
import time

import tweepy

from dotenv import load_dotenv
import os

from tqdm import tqdm
from tweepy import TweepyException

from utils import divide_chunks

load_dotenv()  # load environment variables from .env

USER_FIELDS = ['created_at', 'description', 'entities', 'id', 'location', 'name', 'pinned_tweet_id',
               'profile_image_url', 'protected', 'public_metrics', 'url', 'username', 'verified', 'withheld']
BATCH_SIZE = 100
FOLLOWEES_PER_CALL = 5000
FOLLOWERS_PER_CALL = 5000


def get_api():
    auth = tweepy.OAuth2BearerHandler(
        bearer_token=os.environ['BEARER'])
    return tweepy.API(auth, wait_on_rate_limit=True)


def get_client():
    return tweepy.Client(bearer_token=os.environ['BEARER'],
                         wait_on_rate_limit=True, )


def get_profiles(ids, client, out_path, error_path, user_fields=USER_FIELDS, batch_size=BATCH_SIZE):
    errors = list()

    with open(out_path, 'a+', encoding='utf8') as f, open(error_path, 'a+', encoding='utf8') as err:

        for chunk in tqdm(divide_chunks(ids, batch_size), desc='batch',
                          total=len(ids) // batch_size + bool(len(ids) % batch_size)):
            try:
                returned = client.get_users(ids=chunk, user_fields=user_fields)
                for user in returned.data:
                    f.write(json.dumps(user.data) + '\n')
                for error in returned.errors:
                    err.write(json.dumps(error) + '\n')
            except TweepyException as e:
                print(e)
                errors.extend(chunk)
                time.sleep(60)
    return errors


def get_followee_lists(author_ids, out_path, api):
    exception_users = dict()
    with open(out_path, 'a+', encoding='utf8') as f:
        for author_id in tqdm(author_ids, desc='checking followees'):
            followee_ids = []
            try:
                for page in tweepy.Cursor(api.get_friend_ids, user_id=author_id, count=FOLLOWEES_PER_CALL).pages():
                    followee_ids.extend(page)
                f.write(json.dumps({author_id: followee_ids}) + '\n')
            except TweepyException as e:
                print(e)
                print(author_id)
                exception_users[author_id] = e
    return exception_users


def get_follower_lists(author_ids, out_path, api):
    exception_users = dict()
    with open(out_path, 'a+', encoding='utf8') as f:
        for author_id in tqdm(author_ids, desc='checking followers'):
            follower_ids = []
            try:
                for page in tweepy.Cursor(api.get_follower_ids, user_id = author_id, count =FOLLOWERS_PER_CALL).pages():
                    follower_ids.extend(page)
                f.write(json.dumps({author_id:follower_ids}) + '\n')
            except TweepyException as e:
                print(e)
                print(author_id)
                exception_users[author_id]=e
    return exception_users