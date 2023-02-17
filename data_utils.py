import json
import os

DATA_PATH = 'data'
YEARS = [2016, 2020]


def get_scaraped_profiles(out_path=os.path.join(DATA_PATH, 'followers_rehydrated.jsonl'),
                          err_path=os.path.join(DATA_PATH, 'followers_missing.jsonl')):
    already_scraped = set()
    if os.path.exists(out_path):
        with open(out_path) as f:
            already_scraped = {json.loads(l)['id'] for l in f}
    if os.path.exists(err_path):
        with open(err_path) as f:
            already_scraped.update({json.loads(l)['resource_id'] for l in f})
    already_scraped = set(map(int, already_scraped))
    return already_scraped


def get_retweeters_repliers():
    repliers = set()
    for year in YEARS:
        with open(os.path.join(DATA_PATH, f'retweet_{year}.json')) as f:
            retweeters_of = json.load(f)
            for retweeters in retweeters_of.values():
                for retweeter in retweeters:
                    repliers.add(retweeter['id'])
        with open(os.path.join(DATA_PATH, f'reply_{year}.json')) as f:
            replies_of = json.load(f)
            for replies in replies_of.values():
                for reply in replies:
                    repliers.add(reply['author_id'])
    return list(sorted(repliers))


def get_followers_from_lists():
    ids = set()
    for year in YEARS:
        with open(os.path.join(DATA_PATH, f'follower_lists_{year}.jsonl')) as f:
            for l in f:
                for _, ids_ in json.loads(l).items():
                    ids.update(ids_)
    return sorted(list(ids))


def get_authors_from_follower_lists(out_path):
    existing_users = set()
    if os.path.exists(out_path):
        with open(out_path) as f:
            existing_users.update(k for l in f for k in json.loads(l))
    return list(sorted(existing_users))


def get_authors_from_keys(fpath):
    with open(fpath) as f:
        author_ids = [id for id in json.load(f)]
    return author_ids


def get_author_ids(year, save=False):
    with open(os.path.join(DATA_PATH, f'polls-{year}.json')) as f:
        polls = json.load(f)
    author_ids = [poll['meta']['author_id'] for poll in filter(lambda x: x['type'] == 'twitter', polls)]
    if save:
        with open(os.path.join(DATA_PATH, f'polls_{year}_author_ids.json'), 'w+') as f:
            json.dump(author_ids, f)
    return author_ids


def write_error_users(exception_users, fpath):
    with open(fpath, 'a+') as f:
        for k, v in exception_users.items():
            f.write(json.dumps({k: v.api_errors[0]}) + '\n')


def read_error_users(fpath):
    return get_authors_from_follower_lists(fpath)
