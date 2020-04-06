
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
                petrol_station_and_should = address_has_word_station or 'דלק' in str(original_address)
            if 'AUTOMOTIVE_DEALER' in classification_codes:
                automotive_dealer_and_should = address_has_word_car

    return bus_station_and_should and train_station_and_should and petrol_station_and_should \
           and automotive_dealer_and_should


def rate_locations(locations):
    def rate_location(location):
        if "score" in location.raw:
            return location.raw["score"]
        raise Exception()

    try:
        return list(map(lambda location: (location, rate_location(location)), locations))
    except Exception:
        locations_len = len(locations)
        return list([(location, locations_len - i) for i, location in enumerate(locations)])


def filter_and_rate(locations, original_address):
    if locations:
        filtered_locations = list(filter(lambda location: keep_location_azure(location, original_address), locations))
        if filtered_locations:
            locations_score = rate_locations(filtered_locations)
            return locations_score
    return []


def get_classifications(location):
    if 'poi' in location.raw and 'classifications' in location.raw['poi']:
        classifications = location.raw['poi']['classifications']
        return list(map(lambda classif: classif['code'], classifications))
    return []
