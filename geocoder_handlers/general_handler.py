from fuzzywuzzy import fuzz

from utils.TranslationHandler import translate_if_needed


def rate_location(location, original_address):
    fixed_location = translate_if_needed(location.address)
    return fuzz.token_sort_ratio(original_address, fixed_location)


def choose_location(locations, original_address):
    if locations:
        location_score = map(lambda location: (location, rate_location(location, original_address)), locations)

        result = max(location_score, key=lambda loc_scr: loc_scr[1])
        return result[0]
    return None


def get_classifications(location):
    return []
