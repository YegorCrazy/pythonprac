import gettext, sys, os

apath = os.path.join(os.path.dirname(__file__), 'a')
translation = gettext.translation('a', apath, fallback=True)
_, ngettext = translation.gettext, translation.ngettext

while a := sys.stdin.readline():
    a = a.split()
    print(ngettext('{} word entered', '{} words entered', len(a)).format(len(a)))
