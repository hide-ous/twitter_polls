# twitter_polls

1. create a virtual environment, activate it, and `pip install -r requirements.txt`
2. create a `.env` file in the project root and add `BEARER=YOUR_TWITTER_BEARER`
3. create a `data` folder in the project root and place `polls-{year}.json` in it
4. run `get_follower_lists.ipynb` to generate `polls_{year}_author_ids.json` and `follower_lists_{year}.jsonl`
5. run `get_followers.ipynb` to generate `followers_rehydrated.jsonl`
6. install a local nominatim server
    ```cmd
    docker run -it --shm-size=16g -e PBF_URL=https://ftp5.gwdg.de/pub/misc/openstreetmap/planet.openstreetmap.org/pbf/planet-latest.osm.pbf  -p 8080:8080  -e IMPORT_STYLE=admin  -e FREEZE=true -e USER_AGENT="nominatim_v0.0.1" -e IMPORT_WIKIPEDIA=true  -e IMPORT_US_POSTCODES=true   -e IMPORT_GB_POSTCODES=true  -e IMPORT_TIGER_ADDRESSES=true  -v "E:\nominatim\data":/var/lib/postgresql/14/main  -v "E:\nominatim\flat":/nominatim/flatnode  --name nominatim  mediagis/nominatim:4.2
    ```
7. run `geocode_from_bios.ipynb`


### TODO:
- [x] parse poll files to extract unique authors
- [x] re-scrape follower lists for authors 
- [ ] scrape profiles for followers of authors, repliers, retweeters, quoters 
- [x] log error codes associated with missing accounts
- [ ] scrape followee lists for repliers, retweeters, quoters
- [ ] scrape follower lists for congress members
- [ ] geocode all locations
