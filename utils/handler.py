import time

from models.geo_locator_result import GeoLocationResult


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


def get_results_from_geolocators(geolocators, curr_address, x=None, y=None):
    """
    Uses the geolocators to get results for curr_address from every geolocator by the highest scored location
    If passing x and y the result from every geolocator will be chosen by the match to Point(x,y) and then highest score
    :param geolocators:
    :param curr_address:
    :param x:
    :param y:
    :rtype: list<GeoLocationResult>
    """
    locators_locations = use_all_locators(geolocators, curr_address)
    return list(map(lambda locator_locations: get_location_result(locator_locations, curr_address), locators_locations))


def get_location_result(locator_locations, curr_address, x=None, y=None):
    """
    Choose and create result for curr_address from locator_locations by the highest scored result.
    If passing x and y the location result from the locator_locations will be chosen by the match to Point(x,y)
    and then by highest score
    :param locator_locations:
    :param curr_address:
    :param x:
    :param y:
    :return: GeoLocationResult
    """
    locator = locator_locations[0]
    scored_locations = locator.filter_rate_locations(locator_locations[1], curr_address)
    geo_location_results_scored = list(map(lambda location_score: (create_GeoLocationResult(location_score[0], locator),
                                                                   location_score[1]), scored_locations))
    if x is None or y is None:
        location = get_max_rated_location(geo_location_results_scored)
    else:
        location = get_close_location_max_score(geo_location_results_scored, x, y)
    if location is not None:
        return location
    return None


def get_close_location_max_score(geo_location_results_scored, x, y):
    geo_location_results_scored_filtered = \
        filter(lambda geo_location: geo_location.match(x, y), geo_location_results_scored)
    return get_max_rated_location(geo_location_results_scored_filtered)


def create_GeoLocationResult(location, locator):
    classifications = locator.get_classifications(location)
    return GeoLocationResult(
        address=location.address,
        x=location.longitude,
        y=location.latitude,
        classifications=classifications if not None else [],
        locator_name=locator.name
    )


def get_max_rated_location(geo_location_results_scored):
    if geo_location_results_scored:
        result = max(geo_location_results_scored, key=lambda loc_scr: loc_scr[1])
        return result[0]
    return None
