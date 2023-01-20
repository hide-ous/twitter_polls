# twitter_polls

1. create a virtual environment, activate it, and `pip install -r requirements.txt`
2. create a `.env` file in the project root and add `BEARER=YOUR_TWITTER_BEARER`
3. create a `data` folder in the project root and place `polls_{year}_labeled.json` in it
4. run `get_follower_lists.ipynb` to generate `polls_{year}_author_ids.json` and `follower_lists_{year}.jsonl`
5. run `get_followers.ipynb` to generate `followers_{year}_rehydrated.jsonl`
6. run `geocode_from_bios.ipynb`