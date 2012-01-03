import gettext
import locale
from gtk import glade
LOCALE_PATH = "/usr/share/locale"
#LOCALE_PATH = "@datadir@/locale"
GETTEXT_DOMAIN = 'whatsup'
locale.setlocale(locale.LC_ALL, '')
for module in glade, gettext:
    module.bindtextdomain(GETTEXT_DOMAIN, LOCALE_PATH)
    module.textdomain(GETTEXT_DOMAIN)

# register the gettext function for the whole interpreter as "_"
import __builtin__
__builtin__._ = gettext.gettext

APPNAME = "friendly"
ICON_PATH = "../friendly/data/whatsup.png"