import os
from functools import partial

import pandas as pd

from geopy.exc import GeocoderUnavailable
from geopy.geocoders import Nominatim
from ratelimit import limits, sleep_and_retry

DUMMY_LOCATION_STRS = ["Berlin, Deutschland",
                       "France",
                       "Paris et plein Centre",
                       "Punjab, Pakistan",
                       "South Africa",
                       "Boulder, Colorado",
                       "NONE",
                       "London",
                       "United States",
                       "Ethiopia",
                       "Ethiopia",
                       "TΧ",
                       "NONE",
                       "Paris, Mulhouse, sur la route",
                       "London",
                       "Barcelona",
                       "Liverpool",
                       "Bay Area, CA"]


@sleep_and_retry
@limits(calls=1, period=1)
def get_location(location_str, geolocator, **kwargs):
    try:
        return geolocator.geocode(location_str, **kwargs)
    except GeocoderUnavailable as e:
        return None


def read_locations():  # TODO: update to real data
    return pd.DataFrame(DUMMY_LOCATION_STRS, columns=['location_str'], index=range(len(DUMMY_LOCATION_STRS)))


@sleep_and_retry
@limits(calls=1, period=1)
def reverse_location(location_obj, geolocator, **kwargs):
    try:
        coords = ",".join((location_obj.raw['lat'], location_obj.raw['lon']))
    except AttributeError as e:
        return None
    try:
        return geolocator.reverse(coords, **kwargs)
    except GeocoderUnavailable as e:
        return None


if __name__ == '__main__':
    # read the data
    locations = read_locations()
    # initialize the geolocator service
    geolocator = Nominatim(user_agent="twitter_poll_bio_geocoding_v0.0.1")

    # apply the geolocator
    locations['location_obj'] = locations.location_str.apply(partial(get_location, geolocator=geolocator))

    # apply the reverse geolocator
    locations['location_obj_reversed'] = locations.location_obj.apply(partial(reverse_location, geolocator=geolocator))

    # unpack address information
    addresses = pd.DataFrame(locations.location_obj_reversed.dropna().apply(lambda x: pd.Series(x.raw['address'])))

    # merge with the original dataframe
    locations = pd.merge(locations, addresses, left_index=True, right_index=True)

    # save data
    locations[['location_str', 'country_code']].to_csv(os.path.join('data', 'bio_country_codes.csv'))
    locations[['location_str', 'railway',
               'road', 'suburb', 'borough', 'city', 'ISO3166-2-lvl4', 'postcode',
               'country', 'country_code', 'village', 'municipality', 'county',
               'ISO3166-2-lvl6', 'state', 'region', 'subdistrict', 'house_number',
               'tourism', 'neighbourhood', 'ISO3166-2-lvl8', 'state_district',
               'quarter', 'city_district']].to_csv(os.path.join('data', 'bio_locations.csv'))
    locations.to_pickle(os.path.join('data', 'bio_locations.pkl'))
