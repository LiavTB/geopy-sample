from fuzzywuzzy import fuzz

from utils.TranslationHandler import translate_if_needed


def keep_location_azure(location, original_address):
    bus_station_and_should = True
    train_station_and_should = True
    petrol_station_and_should = True
    automotive_dealer_and_should = True

    if 'poi' in location.raw:
        if 'classifications' in location.raw['poi']:
            classifications = location.raw['poi']['classifications']
            classification_codes = list(map(lambda classification: classification['code'], classifications))
            address_has_word_station = 'תחנת' in str(original_address) or 'תחנה' in str(original_address) \
                                       or 'התחנה' in str(original_address) or 'התחנת' in str(original_address)

            address_has_word_car = 'מכונית' in str(original_address) or 'מכוניות' in str(original_address) \
                                   or 'רכב' in str(original_address) or 'רכבים' in str(original_address) \
                                   or 'אוטו' in str(original_address)

            if 'PUBLIC_TRANSPORT_STOP' in classification_codes:
                bus_station_and_should = address_has_word_station or 'אוטובוס' in str(original_address)
            if 'RAILWAY_STATION' in classification_codes:
                train_station_and_should = address_has_word_station or 'רכבת' in str(original_address)
            if 'PETROL_STATION' in classification_codes:
                train_station_and_should = address_has_word_station or 'דלק' in str(original_address)
            if 'AUTOMOTIVE_DEALER' in classification_codes:
                automotive_dealer_and_should = address_has_word_car

    return bus_station_and_should and train_station_and_should and petrol_station_and_should \
           and automotive_dealer_and_should


# Azure
def rate_location(location, original_address):
    if 'extendedPostalCode' in location.raw['address']:
        postal_code = location.raw['address']['extendedPostalCode']
    else:
        postal_code = ''
    location_address_no_postal = location.address.replace(postal_code, '')

    if 'poi' in location.raw:
        name = location.raw['poi']['name']
    else:
        name = ''
    location_address_with_name = location_address_no_postal + name

    location_address_fixed = translate_if_needed(location_address_with_name)
    return (location, fuzz.token_set_ratio(original_address, location_address_fixed))


def choose_location(locations, original_address):
    filtered_locations = list(filter(lambda location: keep_location_azure(location, original_address), locations))
    if filtered_locations:
        return filtered_locations[0]
    return None


def get_classifications(location):
    if 'poi' in location.raw and 'classifications' in location.raw['poi']:
        classifications = location.raw['poi']['classifications']
        return list(map(lambda classif: classif['code'], classifications))
    return []
