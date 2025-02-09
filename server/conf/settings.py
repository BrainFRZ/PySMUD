r"""
Evennia settings file.

The available options are found in the default settings file found
here:

https://www.evennia.com/docs/latest/Setup/Settings-Default.html

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################
from utils import tick_colors


# This is the name of your game. Make it catchy!
SERVERNAME = "SuperMUD"

# Assign the settings variables
COLOR_ANSI_EXTRA_MAP = tick_colors.TICK_COLOR_ANSI_EXTRA_MAP
COLOR_XTERM256_EXTRA_FG = tick_colors.TICK_COLOR_XTERM256_EXTRA_FG
COLOR_XTERM256_EXTRA_BG = tick_colors.TICK_COLOR_XTERM256_EXTRA_BG
COLOR_XTERM256_EXTRA_GFG = tick_colors.TICK_COLOR_XTERM256_EXTRA_GFG
COLOR_XTERM256_EXTRA_GBG = tick_colors.TICK_COLOR_XTERM256_EXTRA_GBG
COLOR_ANSI_BRIGHT_BG_EXTRA_MAP = tick_colors.TICK_COLOR_ANSI_XTERM256_BRIGHT_BG_EXTRA_MAP


######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
