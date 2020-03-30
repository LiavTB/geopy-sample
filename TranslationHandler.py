# -*- coding: utf-8 -*-
from translate import Translator


def is_english(s):
    try:
        s.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True


def translate_en_he(string11):
    translator = Translator(to_lang='he', from_lang='en')
    return translator.translate(text=string11)


def translate_if_needed(address):
    if is_english(address):
        return translate_en_he(address)
    return address
