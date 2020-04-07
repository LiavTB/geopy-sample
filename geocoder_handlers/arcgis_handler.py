from geocoder_handlers import general_handler
from geocoder_handlers import handler_utils


def keep_location(location):
    attributes = location.raw['attributes']
    return attributes['Country'] == 'ISR' and attributes['Addr_type'] != 'Locality' and \
           attributes['Addr_type'] != 'StreetName'


def filter_and_rate(locations, original_address):
    if locations:
        filtered_locations = list(filter(lambda location: keep_location(location), locations))
        if filtered_locations:
            locations_score = map(lambda location: (location, handler_utils.rate_location(location, original_address)), filtered_locations)

            # result = max(location_score, key=lambda loc_scr: loc_scr[1])
            return locations_score
    return []


def get_classifications(location):
    classifications = []
    if 'attributes' in location.raw and 'Addr_type' in location.raw['attributes']:
        if location.raw['attributes']['Addr_type'] == 'POI':
            classifications.append(location.raw['attributes']['Type'])
    return classifications