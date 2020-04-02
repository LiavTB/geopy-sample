from geopy.exc import GeocoderNotFound
from geopy.geocoders import SERVICE_TO_GEOCODER

from custom_geocoders.azure_fuzzy import AzureMapsFuzzy


__all__ = (
    "get_custom_geocoder",
    # The order of classes below should correspond to the order of their
    # files in the ``geocoders`` directory ordered by name.
    "AzureMapsFuzzy",
)

CUSTOM_SERVICE_TO_GEOCODER = {
"azurefuzzy": AzureMapsFuzzy
}


def get_custom_geocoder(service):
    """
    For the service provided, try to return a geocoder class.

    If the string given is not recognized, a
    :class:`geopy.exc.GeocoderNotFound` exception is raised.
    """
    try:
        return CUSTOM_SERVICE_TO_GEOCODER[service.lower()]
    except KeyError:
        raise GeocoderNotFound(
            "Unknown geocoder '%s'; options are: %s" %
            (service, SERVICE_TO_GEOCODER.keys() + CUSTOM_SERVICE_TO_GEOCODER.keys())
        )
