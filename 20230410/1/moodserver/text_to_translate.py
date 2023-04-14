"""
This module stores text that should be translated to help pybabel see it.

To see where this text is used in a module please use grep.
"""


def _(arg):
    return arg


def ngettext(arg):
    """Make pybabel think that we translate some stuff."""
    return arg


text_to_translate = [
    _('{} was connected'),
    _('{} was disconnected'),
    _('right'),
    _('left'),
    _('up'),
    _('down'),
    _('sword'),
    _('spear'),
    _('axe'),
    _('{} moved one cell {}'),
    _('Added monster to ({}, {}) saying {}'),
    _('Added monster to ({}, {}) saying {}\nReplaced the old monster'),
    _('{} added monster to ({}, {}) saying {}'),
    _('{} added monster to ({}, {}) saying {} and replaced the old monster'),
    _('No {} here'),
    _('Attacked {} with {}, damage {} {}'),
    _('{} attacked {} with {}, damage {} {}'),
    _('{} died'),
    _('{} now has {} {}'),
    _('Moved to ({}, {})'),
    _('Set {} locale'),
    ]

text_to_ntranslate = [
    ngettext('hp', 'hp', 7)
    ]
