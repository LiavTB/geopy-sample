# -*- coding: utf-8 -*-
import pandas as pd
import time
from fuzzywuzzy import fuzz

from models.GeoLocator import GeoLocator
from TranslationHandler import translate_if_needed


def use_all_locators(geolocators, address):
    locations = []
    for geolocator in geolocators:
        location = None
        retries_left = 6
        while retries_left != 0:
            try:
                # if geolocator.api_key is not None:
                #     location = geolocator.locator.geocode(query=address, api_key=geolocator.api_key)
                # else:
                location = geolocator.locator[0].geocode(query=address, exactly_one=False)
                retries_left = 0
            except Exception as e:
                print(e)
                print('retries_left: ' + str(retries_left))
                time.sleep(2)
                retries_left = retries_left - 1

        if location is not None:
            locations.append((geolocator.name, location))
    return locations


def is_english(s):
    try:
        s.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True


def choose_location(locations, original_address):
    location_score = map(lambda location: (location, fuzz.token_sort_ratio(original_address, translate_if_needed(location.address))),
                        locations)
    result = max(location_score, key=lambda loc_scr: loc_scr[1])
    return result[0]


if __name__ == '__main__':
    print("start_time: " + str(time.strftime("%I:%M:%S %p", time.localtime())))

    geocoders_names = [("Nominatim", {}),
                       ("Photon", {}),
                       ("ArcGIS", {}),
                       # TODO - SET api_key FOR "Bing" SERVICE (can be generated from Bing map service)
                       ("Bing", {"api_key": "API_KEY_TO_SET"}),
                       # TODO - SET username FOR "geonames" SERVICE (can be generated from geonames service)
                       ("geonames", {"username": "USERNAME_TO_SET"})
                       ]

    geolocators = list(map(lambda name_settings: GeoLocator(name_settings[0], name_settings[1]), geocoders_names))

    wanted_result = pd.read_csv('./output_wanted_result_example/exposure_locations.csv')
    # wanted_result_shorted = wanted_result[['x', 'y', 'מקום']]
    wanted_result_shorted = wanted_result

    new_results = []

    counter = 0

    for i, row in wanted_result_shorted.iterrows():
        counter = counter + 1
        print('counter: ' + str(counter))
        curr_address = row['מקום']
        address_locations = use_all_locators(geolocators, curr_address)
        print(str(time.strftime("%I:%M:%S %p", time.localtime())))
        for locations in address_locations:
            location = choose_location(locations[1], curr_address)
            wanted_result_shorted.at[i, str(locations[0]) + '_address'] = location.address
            wanted_result_shorted.at[i, str(locations[0]) + '_x'] = location.longitude
            wanted_result_shorted.at[i, str(locations[0]) + '_y'] = location.latitude
        print()

    print("end_time: " + str(time.strftime("%I:%M:%S %p", time.localtime())))
    wanted_result_shorted.to_csv('./output_wanted_result_example/test_result_5_wuzzy.csv')

    # address = "בית כנסת אבני חושן שכונת קייזר מודיעין"
    # address2 = "קניון רחובות"
    # address_locations = use_all_locators(geolocators, address)
    # address2_locations = use_all_locators(geolocators, address2)

    print("done")
