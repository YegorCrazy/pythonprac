import gettext, os

apath = os.path.join(os.path.dirname(__file__), 'l10n')
translation = gettext.translation('l10n', apath, fallback=True)
_, ngettext = translation.gettext, translation.ngettext

directions_translated_dict = {
    'right': _('right'),
    'left': _('left'),
    'up': _('up'),
    'down': _('down')
    }

weapons_names_translated_dict = {
    'sword': _('sword'),
    'spear': _('spear'),
    'axe': _('axe')
    }
