from fuzzywuzzy import fuzz

from utils.TranslationHandler import translate_if_needed


def rate_location(location, original_address):
    fixed_location = translate_if_needed(location.address)
    return fuzz.token_sort_ratio(original_address, fixed_location)