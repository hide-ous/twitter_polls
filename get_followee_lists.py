import json
import pickle

from tqdm import tqdm
import tweepy
from dotenv import load_dotenv
import os

from tweepy import TweepyException

load_dotenv()  # load environment variables from .env

DATA_PATH = 'data'
YEARS = [2016, 2020]

auth = tweepy.OAuth2BearerHandler(
    bearer_token= os.environ['BEARER'])
api = tweepy.API(auth, wait_on_rate_limit=True)

FOLLOWEES_PER_CALL = 5000
def get_followee_lists(author_ids, out_path, api):
    exception_users = dict()
    with open(out_path, 'a+', encoding='utf8') as f:
        for author_id in tqdm(author_ids, desc='checking followers'):
            followee_ids = []
            try:
                for page in tweepy.Cursor(api.get_friend_ids, user_id = author_id, count = FOLLOWEES_PER_CALL).pages():
                    followee_ids.extend(page)
                f.write(json.dumps({author_id:followee_ids}) + '\n')
            except TweepyException as e:
                print(e)
                print(author_id)
                exception_users[author_id]=e
    return exception_users


if __name__ == '__main__':

    replies = dict()
    for fname in ['reply_2016.json', 'reply_2020.json', 'retweet_2016.json', 'retweet_2020.json']:
        with open(os.path.join(DATA_PATH, fname)) as f:
            replies.update(json.load(f))

    repliers = set(filter(lambda x: x is not None, [vv.get('id', None) for k, v in replies.items() for vv in v]))
    repliers = list(sorted(repliers))[::-1]

    exception_users = dict()
    out_path = os.path.join(DATA_PATH, f'followee_lists_of_repliers.jsonl')
    exception_users.update(get_followee_lists(repliers, out_path, api))
    if len(exception_users):
        with open(os.path.join(DATA_PATH, 'replier_errors.pkl'), "wb+") as f:
            pickle.dump(exception_users)