# -*- coding: utf-8 -*-
import math
import pandas as pd
import time
from geopy.distance import great_circle

from models.GeoLocator import GeoLocator
from geocoder_handlers import azure_handler, arcgis_handler


def use_all_locators(geolocators, address):
    locator_locations = []
    for geolocator in geolocators:
        location = None
        retries_left = 6
        while retries_left != 0:
            try:
                location = geolocator.locator.geocode(query=address, exactly_one=False, **geolocator.geocode_args)
                retries_left = 0
            except Exception as e:
                print(e)
                print('retries_left: ' + str(retries_left))
                time.sleep(2)
                retries_left = retries_left - 1

        if location is not None:
            locator_locations.append((geolocator, location))
    return locator_locations


if __name__ == '__main__':
    print("start_time: " + str(time.strftime("%I:%M:%S %p", time.localtime())))

    geolocators = [
        # GeoLocator(geocoder_name="Nominatim"),
        # GeoLocator(geocoder_name="Photon"),
        # GeoLocator(geocoder_name="ArcGIS",
        #            geocode_args={"out_fields": "*"},
        #            choose_location_func=arcgis_handler.choose_location),
        # # TODO - SET subscription_key FOR "azure" SERVICE (can be generated from azure map service)
        GeoLocator(geocoder_name="azurefuzzy",
                   settings={"subscription_key": "YkXx4mKTp9sldPyL_xeAZIAmvbi9ZsT1TJnT1zQopnQ"},
                   geocode_args={'typeahead': True},
                   choose_location_func=azure_handler.choose_location,
                   get_classifications_func=azure_handler.get_classifications),
        # # TODO - SET api_key FOR "Bing" SERVICE (can be generated from Bing map service)
        # GeoLocator(geocoder_name="Bing",
        #            settings={"api_key": "Aivwx7buZEuTGt8t0ZlCI4YB7zHFTWmbqC6qLXqIQ1flPU7KJoslecVu9hj1O2i3"}),
        # # # TODO - SET username FOR "geonames" SERVICE (can be generated from geonames service)
        # GeoLocator(geocoder_name="geonames",
        #            settings={"username": "temp_use1234555"})
    ]

    # CSV
    # TODO - Set the file path to read from
    # exposure_locations_original_csv = './output_wanted_result_example/Corona_exposure_locations.csv'
    # output_csv_base = './output_wanted_result_example/test_result_arcgis{}.csv'
    # service_output_csv = output_csv_base.format("")
    # service_output_close_csv = output_csv_base.format("_close")
    # location_col_name = 'מקום'
    # wanted_result = pd.read_csv(exposure_locations_original_csv)

    # Excel
    # TODO - Set the file path to read from
    exposure_locations_original_excel = './big_data/EPI_CoronaExposure_XRM_NEW_31_3_1807_TableToExcel.xlsx'
    output_csv_base = './big_data/test_result_azure_2_try{}.csv'
    service_output_csv = output_csv_base.format("")
    service_output_close_csv = output_csv_base.format("_close")
    location_col_name = 'place'
    wanted_result = pd.read_excel(exposure_locations_original_excel)

    geocoder_x_suffix = '_x'
    geocoder_y_suffix = '_y'
    geocoder_classification = '_classification'

    # # Use All the GeoLocators to find the locations

    for i, row in wanted_result.iterrows():
        print('counter: ' + str(i + 1))
        curr_address = row[location_col_name]
        if str(curr_address) != 'nan':
            locator_locations = use_all_locators(geolocators, curr_address)
            print(str(time.strftime("%I:%M:%S %p", time.localtime())))
            print('searching location for: ' + str(curr_address))
            for locator_locations in locator_locations:
                locator = locator_locations[0]
                location = locator.choose_location(locator_locations[1], curr_address)
                if location is not None:
                    print('the location found is: ' + str(location.address))
                    wanted_result.at[i, str(locator.name) + '_address'] = location.address
                    wanted_result.at[i, str(locator.name) + geocoder_x_suffix] = location.longitude
                    wanted_result.at[i, str(locator.name) + geocoder_y_suffix] = location.latitude
                    wanted_result.at[i, str(locator.name) + geocoder_classification] = \
                        '[' + ','.join(locator.get_classifications(location)) + ']'
        print()

    print("end_time: " + str(time.strftime("%I:%M:%S %p", time.localtime())))
    wanted_result.to_csv(service_output_csv)

    # # Add the CHECK FOR CLOSE LOCATIONS OF X and Y

    # CSV
    # org_x_suffix = 'x'
    # org_y_suffix = 'y'

    # Excel
    org_x_suffix = 'POINT_X'
    org_y_suffix = 'POINT_Y'

    distance_suffix = '_distance'
    close_suffix = '_close'

    check_result = pd.read_csv(service_output_csv)
    for i, row in check_result.iterrows():
        counter = i
        print('counter: ' + str(counter))
        print(str(time.strftime("%I:%M:%S %p", time.localtime())))
        for geolocator in geolocators:
            name = str(geolocator.name)
            if name + geocoder_x_suffix in row:
                longitude = float(row[name + geocoder_x_suffix])
                latitude = float(row[name + geocoder_y_suffix])
                longitude_org = float(row[org_x_suffix])
                latitude_org = float(row[org_y_suffix])
                if math.isnan(longitude):
                    check_result.at[i, name + close_suffix] = ''
                else:
                    point_found = (latitude, longitude)
                    point_original = (latitude_org, longitude_org)
                    distance = great_circle(point_original, point_found).meters

                    check_result.at[i, name + distance_suffix] = distance
                    check_result.at[i, name + close_suffix] = distance <= 50
        print()
    check_result.to_csv(service_output_close_csv)

    # # SUM the CLOSED LOCATIONS
    sum_true = 0
    sum_true_2_plus = 0
    check_result = pd.read_csv(service_output_close_csv)
    for i, row in check_result.iterrows():
        counter = i
        print('counter: ' + str(counter))
        print(str(time.strftime("%I:%M:%S %p", time.localtime())))
        true_count = 0
        for geolocator in geolocators:
            name = str(geolocator.name) + close_suffix
            if name in row:
                close = str(row[name])
                # if close == 'True' or close == 'False':
                if close == 'True':
                    true_count = true_count + 1
        if true_count > 0:
            sum_true = sum_true + 1
        if true_count > 1:
            sum_true_2_plus = sum_true_2_plus + 1

    print('sum_true: ' + str(sum_true))
    print('sum_true_2_or_more: ' + str(sum_true_2_plus))

    print("done")
