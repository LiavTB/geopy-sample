from geocoder_handlers import handler_utils


def filter_and_rate(locations, original_address):
    if locations:
        locations_score = map(lambda location: (location, handler_utils.rate_location(location, original_address)),
                              locations)
        return locations_score
    return []


def get_classifications(location):
    return []
