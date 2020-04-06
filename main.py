# -*- coding: utf-8 -*-
import pandas as pd

import pandas_to_csv_logic
from models.GeoLocator import GeoLocator
from geocoder_handlers import azure_handler, arcgis_handler

if __name__ == '__main__':
    geolocators = [
        GeoLocator(geocoder_name="Nominatim"),
        GeoLocator(geocoder_name="Photon"),
        GeoLocator(geocoder_name="ArcGIS",
                   geocode_args={"out_fields": "*"},
                   filter_rate_locations_func=arcgis_handler.filter_and_rate),
        # # TODO - SET subscription_key FOR "azure" SERVICE (can be generated from azure map service)
        GeoLocator(geocoder_name="azurefuzzy",
                   settings={"subscription_key": ""},
                   geocode_args={'typeahead': True},
                   filter_rate_locations_func=azure_handler.filter_and_rate,
                   get_classifications_func=azure_handler.get_classifications),
        # # TODO - SET api_key FOR "Bing" SERVICE (can be generated from Bing map service)
        GeoLocator(geocoder_name="Bing",
                   settings={"api_key": ""}),
        # # # TODO - SET username FOR "geonames" SERVICE (can be generated from geonames service)
        GeoLocator(geocoder_name="geonames",
                   settings={"username": ""})
    ]

    # CSV
    # TODO - Set the file path to read from
    # exposure_locations_original_csv = ''
    # TODO - Set the output file path to write
    # service_output_csv = ''
    # location_col_name = 'מקום'
    # org_x_suffix = 'x'
    # org_y_suffix = 'y'
    # df = pd.read_csv(exposure_locations_original_csv)

    # Excel
    # TODO - Set the file path to read from
    exposure_locations_original_excel = ''

    # TODO - Set the output file path to write
    service_output_csv = ''
    location_col_name = 'place'
    org_x_suffix = 'POINT_X'
    org_y_suffix = 'POINT_Y'
    df = pd.read_excel(exposure_locations_original_excel)

    pandas_to_csv_logic.run(df, geolocators, location_col_name, org_x_suffix, org_y_suffix, service_output_csv)

    print()



    print("done")
