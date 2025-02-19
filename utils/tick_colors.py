"""
Color markups

Contribution, Griatch 2017

Additional color markup styles for Evennia (extending or replacing the default |r, |234 etc).


Installation:

Import the desired style variables from this module into mygame/server/conf/settings.py and add them
to these settings variables. Each are specified as a list, and multiple such lists can be added to
each variable to support multiple formats. Note that list order affects which regexes are applied
first. You must restart both Portal and Server for color tags to update.

Assign to the following settings variables:

    COLOR_ANSI_EXTRA_MAP - a mapping between regexes and ANSI colors
    COLOR_XTERM256_EXTRA_FG - regex for defining XTERM256 foreground colors
    COLOR_XTERM256_EXTRA_BG - regex for defining XTERM256 background colors
    COLOR_XTERM256_EXTRA_GFG - regex for defining XTERM256 grayscale foreground colors
    COLOR_XTERM256_EXTRA_GBG - regex for defining XTERM256 grayscale background colors
    COLOR_ANSI_BRIGHT_BG_EXTRA_MAP = ANSI does not support bright backgrounds; we fake
        this by mapping ANSI markup to matching bright XTERM256 backgrounds

    COLOR_NO_DEFAULT - Set True/False. If False (default), extend the default markup, otherwise
        replace it completely.


To add the {- "curly-bracket" style, add the following to your settings file, then reboot both
Server and Portal:

from evennia.contrib.base_systems import color_markups
COLOR_ANSI_EXTRA_MAP = color_markups.CURLY_COLOR_ANSI_EXTRA_MAP
COLOR_XTERM256_EXTRA_FG = color_markups.CURLY_COLOR_XTERM256_EXTRA_FG
COLOR_XTERM256_EXTRA_BG = color_markups.CURLY_COLOR_XTERM256_EXTRA_BG
COLOR_XTERM256_EXTRA_GFG = color_markups.CURLY_COLOR_XTERM256_EXTRA_GFG
COLOR_XTERM256_EXTRA_GBG = color_markups.CURLY_COLOR_XTERM256_EXTRA_GBG
COLOR_ANSI_BRIGHT_BG_EXTRA_MAP = color_markups.CURLY_COLOR_ANSI_BRIGHT_BG_EXTRA_MAP


To add the %c- "mux/mush" style, add the following to your settings file, then reboot both Server
and Portal:

from evennia.contrib.base_systems import color_markups
COLOR_ANSI_EXTRA_MAP = color_markups.MUX_COLOR_ANSI_EXTRA_MAP
COLOR_XTERM256_EXTRA_FG = color_markups.MUX_COLOR_XTERM256_EXTRA_FG
COLOR_XTERM256_EXTRA_BG = color_markups.MUX_COLOR_XTERM256_EXTRA_BG
COLOR_XTERM256_EXTRA_GFG = color_markups.MUX_COLOR_XTERM256_EXTRA_GFG
COLOR_XTERM256_EXTRA_GBG = color_markups.MUX_COLOR_XTERM256_EXTRA_GBG
COLOR_ANSI_BRIGHT_BGS_EXTRA_MAP = color_markups.CURLY_COLOR_ANSI_BRIGHT_BGS_EXTRA_MAP


"""

"""
Edited by Printer, 2025

* Markup style now uses tick codes instead of curly brackets to match ROM-style color codes.
* MUSH color codes style has been removed as it would be unused.
* Blinking codes have been removed as an option.
* Pure black is now dark grey.
"""


# ANSI constants (copied from evennia.utils.ansi to avoid import)

_ANSI_BEEP = "\07"
_ANSI_ESCAPE = "\033"
_ANSI_NORMAL = "\033[0m"

_ANSI_UNDERLINE = "\033[4m"
_ANSI_HILITE = "\033[1m"
_ANSI_UNHILITE = "\033[22m"
_ANSI_INVERSE = "\033[7m"
_ANSI_INV_HILITE = "\033[1;7m"

# Foreground colors
_ANSI_BLACK = "\033[30m"
_ANSI_RED = "\033[31m"
_ANSI_GREEN = "\033[32m"
_ANSI_YELLOW = "\033[33m"
_ANSI_BLUE = "\033[34m"
_ANSI_MAGENTA = "\033[35m"
_ANSI_CYAN = "\033[36m"
_ANSI_WHITE = "\033[37m"

# Background colors
_ANSI_BACK_BLACK = "\033[40m"
_ANSI_BACK_RED = "\033[41m"
_ANSI_BACK_GREEN = "\033[42m"
_ANSI_BACK_YELLOW = "\033[43m"
_ANSI_BACK_BLUE = "\033[44m"
_ANSI_BACK_MAGENTA = "\033[45m"
_ANSI_BACK_CYAN = "\033[46m"
_ANSI_BACK_WHITE = "\033[47m"

# Formatting Characters
_ANSI_RETURN = "\r\n"
_ANSI_TAB = "\t"
_ANSI_SPACE = " "


#############################################################
#
# `- style MUD markup (matching ROM color codes). This is
# basically identical to the default |-style except using
# a tick mark instead.
#
# `R, `r - bright/dark red foreground
# `[R, `[r - bright/dark red background
# `500, `[500 - XTERM256 red foreground/background
# `=w, `[=w - XTERM256 greyscale foreground/background
#
#############################################################

TICK_COLOR_ANSI_EXTRA_MAP = [
    (r"`x", _ANSI_NORMAL),  # reset
    (r"`/", _ANSI_RETURN),  # line break
    (r"`-", _ANSI_TAB),  # tab
    (r"`_", _ANSI_SPACE),  # space
    (r"`R", _ANSI_HILITE + _ANSI_RED),
    (r"`G", _ANSI_HILITE + _ANSI_GREEN),
    (r"`Y", _ANSI_HILITE + _ANSI_YELLOW),
    (r"`B", _ANSI_HILITE + _ANSI_BLUE),
    (r"`P", _ANSI_HILITE + _ANSI_MAGENTA),
    (r"`M", _ANSI_HILITE + _ANSI_MAGENTA),
    (r"`C", _ANSI_HILITE + _ANSI_CYAN),
    (r"`W", _ANSI_HILITE + _ANSI_WHITE),  # pure white
    (r"`D", _ANSI_HILITE + _ANSI_BLACK),  # dark grey
    (r"`r", _ANSI_UNHILITE + _ANSI_RED),
    (r"`g", _ANSI_UNHILITE + _ANSI_GREEN),
    (r"`y", _ANSI_UNHILITE + _ANSI_YELLOW),
    (r"`b", _ANSI_UNHILITE + _ANSI_BLUE),
    (r"`p", _ANSI_UNHILITE + _ANSI_MAGENTA),
    (r"`m", _ANSI_UNHILITE + _ANSI_MAGENTA),
    (r"`c", _ANSI_UNHILITE + _ANSI_CYAN),
    (r"`w", _ANSI_UNHILITE + _ANSI_WHITE),  # light grey
    (r"`d", _ANSI_HILITE + _ANSI_BLACK),  # switch pure black to dark grey
    # hilight-able colors
    (r"`h", _ANSI_HILITE),
    (r"`H", _ANSI_UNHILITE),
    (r"`!R", _ANSI_RED),
    (r"`!G", _ANSI_GREEN),
    (r"`!Y", _ANSI_YELLOW),
    (r"`!B", _ANSI_BLUE),
    (r"`!M", _ANSI_MAGENTA),
    (r"`!C", _ANSI_CYAN),
    (r"`!W", _ANSI_WHITE),  # light grey
    (r"`!D", _ANSI_BLACK),  # pure black
    # normal ANSI backgrounds
    (r"`[R", _ANSI_BACK_RED),
    (r"`[G", _ANSI_BACK_GREEN),
    (r"`[Y", _ANSI_BACK_YELLOW),
    (r"`[B", _ANSI_BACK_BLUE),
    (r"`[M", _ANSI_BACK_MAGENTA),
    (r"`[C", _ANSI_BACK_CYAN),
    (r"`[W", _ANSI_BACK_WHITE),  # light grey background
    (r"`[D", _ANSI_BACK_BLACK),  # pure black background
]

TICK_COLOR_XTERM256_EXTRA_FG = [r"`([0-9])([0-9])([0-9])"]  # `123 - foreground colour
TICK_COLOR_XTERM256_EXTRA_BG = [r"`\[([0-9])([0-9])([0-9])"]  # `[123 - background colour
TICK_COLOR_XTERM256_EXTRA_GFG = [r"`=([a-z])"]  # `=a - greyscale foreground
TICK_COLOR_XTERM256_EXTRA_GBG = [r"`\[=([a-z])"]  # `[=a - greyscale background

TICK_COLOR_ANSI_XTERM256_BRIGHT_BG_EXTRA_MAP = [
    (r"`[r", r"`[500"),
    (r"`[g", r"`[050"),
    (r"`[y", r"`[550"),
    (r"`[b", r"`[005"),
    (r"`[m", r"`[505"),
    (r"`[c", r"`[055"),
    (r"`[w", r"`[555"),  # white background
    (r"`[d", r"`[222"),  # dark grey background
]
