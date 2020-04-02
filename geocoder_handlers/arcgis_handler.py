from geocoder_handlers import general_handler


def keep_location(location):
    attributes = location.raw['attributes']
    return attributes['Country'] == 'ISR' and attributes['Addr_type'] != 'Locality' and \
           attributes['Addr_type'] != 'StreetName'


def choose_location(locations, original_address):
    filtered_locations = list(filter(lambda location: keep_location(location), locations))
    return general_handler.choose_location(filtered_locations, original_address)
