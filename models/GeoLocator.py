from geopy import get_geocoder_for_service


class GeoLocator:
    def __init__(self, name, settings=None):
        if settings is None:
            settings = {}
        self.name = name,
        self.locator = get_geo_locator(name, settings),


def get_geo_locator(name, settings):
    return get_geocoder_for_service(name)(user_agent='locator_tester', timeout=6, **settings)