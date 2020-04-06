from geopy import get_geocoder_for_service
from geopy.exc import GeocoderNotFound
from custom_geocoders import get_custom_geocoder
from geocoder_handlers import general_handler


class GeoLocator:
    def __init__(self, geocoder_name, settings=None, name=None, geocode_args=None,
                 filter_rate_locations_func=general_handler.filter_and_rate,
                 get_classifications_func=general_handler.get_classifications):
        """
        :param geocoder_name: te geocoder name to get and initialize in the GeoLocator
        :type geocoder_name: str
        :param settings: arguments for the geocoder initialization
        :type settings: dict
        :param name: custom name for the GeoLocator, If not set using the geocoder_name
        :type name: str
        :param geocode_args: arguments for the geocoder.geocode method
        :type geocode_args: dict
        :param filter_rate_locations_func: function to use for filtering and rating locations list
                See for Example `geocoder_handlers.general_handler.filter_and_rate`.
        :param get_classifications_func: function to use to get the classification of location
                See for Example `geocoder_handlers.general_handler.get_classification`.
        """
        if settings is None:
            settings = {}
        if geocode_args is None:
            self.geocode_args = {}
        else:
            self.geocode_args = geocode_args
        if name is None:
            self.name = geocoder_name
        else:
            self.name = name
        self.locator = get_geo_coder(geocoder_name, settings)

        self.filter_rate_locations = filter_rate_locations_func

        self.get_classifications = get_classifications_func


def get_geo_coder(service_name, settings):
    """
            Return a geocoder.
            geocoder is based on the service_name.
            service_name can be custom or default service name.


            :param str service_name: The service name to get GeoLocator.

            :param dict settings:

            :rtype: ``None``, :class:`models.GeoLocator.GeoLocator` or a list of them, if
                ``exactly_one=False``.

            If the service_name string given is not recognized, a
            :class:`geopy.exc.GeocoderNotFound` exception is raised.
            """
    try:
        geocoder = get_geocoder_for_service(service_name)
    except GeocoderNotFound:
        geocoder = get_custom_geocoder(service_name)
    return geocoder(user_agent='locator_tester', timeout=6, **settings)
