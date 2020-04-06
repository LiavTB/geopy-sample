import time

from utils.handler import get_results_from_geolocators


TIME_FORMAT = "%I:%M:%S %p"

geocoder_x_suffix = '_x'
geocoder_y_suffix = '_y'
geocoder_classification = '_classification'
distance_suffix = '_distance'
close_default_suffix = '_close_default'
close_custom_suffix = '_close_custom'
match_suffix = '_match'
match_count_suffix = '_match_count'
min_distance_suffix = '_distance'


# # Use All the GeoLocators to find the locations, calculate the distance and the match
def run(df, geolocators,  location_col_name, org_x_suffix, org_y_suffix, service_output_csv):

    print("start_time: " + str(time.strftime(TIME_FORMAT, time.localtime())))

    for i, row in df.iterrows():
        print('counter: ' + str(i + 1))
        curr_address = row[location_col_name]
        org_x = float(row[org_x_suffix])
        org_y = float(row[org_y_suffix])
        if str(curr_address) != 'nan':
            print('searching location for: ' + str(curr_address))
            geo_location_results = get_results_from_geolocators(geolocators, curr_address)
            print(str(time.strftime(TIME_FORMAT, time.localtime())))
            for geo_location_result in geo_location_results:
                if geo_location_result is not None:
                    name = geo_location_result.locator_name
                    print(str(geo_location_result.locator_name) + ' found: ' + str(geo_location_result.address))
                    df.at[i, str(name) + '_address'] = geo_location_result.address
                    df.at[i, str(name) + geocoder_x_suffix] = geo_location_result.x
                    df.at[i, str(name) + geocoder_y_suffix] = geo_location_result.y
                    df.at[i, str(name) + geocoder_classification] = \
                        '[' + ','.join(geo_location_result.classifications) + ']'
                    df.at[i, name + distance_suffix] = geo_location_result.get_distance(org_x, org_y)
                    df.at[i, name + match_suffix] = geo_location_result.match(org_x, org_y)
            df.at[i, match_count_suffix] = \
                len(list(filter(lambda x: x is not None and x.get_last_match_check() is True, geo_location_results)))
        else:
            df.at[i, match_count_suffix] = -1
        print()

    print("end_time: " + str(time.strftime(TIME_FORMAT, time.localtime())))
    df.to_csv(service_output_csv)
