"""This module contains localization functions and classes."""

import gettext
import os

l10n_path = os.path.join(os.path.dirname(__file__), 'l10n')

supported_languages = ['en', 'ru']

translations = dict()
for language in supported_languages:
    translations[language] = gettext.translation('l10n',
                                                 l10n_path,
                                                 fallback=True,
                                                 languages=[language])


class Translatable:
    """This is a class for storing a string that must be translated."""

    def __init__(self, text):
        self.text = text

    def GetTranslation(self, locale):
        """Get string translation due to locale."""
        if locale not in supported_languages:
            locale = 'en'
        l10n_function = translations[locale].gettext
        return l10n_function(self.text)


class NTranslatable:
    """This class stores a string that must be translated with plural form."""

    def __init__(self, single_text, plural_text, number):
        self.single_text = single_text
        self.plural_text = plural_text
        self.number = number

    def GetTranslation(self, locale):
        """Get string translation due to locale."""
        if locale not in supported_languages:
            locale = 'en'
        l10n_function = translations[locale].ngettext
        return l10n_function(self.single_text, self.plural_text, self.number)


def TranslateWithInsertions(text, insertions, locale):
    """Translate a string with some insertions and format it."""
    if locale not in supported_languages:
        locale = 'en'
    translated_insertions = []
    for insertion in insertions:
        if type(insertion) == Translatable or type(insertion) == NTranslatable:
            translated_insertions.append(insertion.GetTranslation(locale))
        else:
            translated_insertions.append(insertion)
    translated_text = Translatable(text).GetTranslation(locale)
    return translated_text.format(*translated_insertions)
