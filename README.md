# twitter_polls

1. create a virtual environment, activate it, and `pip install -r requirements.txt`
2. create a `.env` file in the project root and add `BEARER=YOUR_TWITTER_BEARER`
3. create a `data` folder in the project root and place `followers_2016.jsonl` in it
4. run `get_followers.ipynb`, or place `followers_2016_rehydrated.jsonl` in `data`
5. run `geocode_from_bios.ipynb`