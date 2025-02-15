"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

from enum import Enum

from evennia.objects.objects import DefaultCharacter

from .objects import ObjectParent


class Eyes(Enum):
    """This enum is used to represent the available colors of a character's eyes."""
    GOLDEN = "`Yg`yo`Yld`ye`Yn`x"
    AMBER = "`172am`166b`172er`x"
    BROWN = "`094br`yo`094wn`x"
    BLUE = "`027bl`026u`027e`x"
    GREEN = "`Ggr`ge`Gen`x"
    GRAY = "`243g`247ra`243y`x"
    HAZEL = "`028ha`058z`028el`x"
    RED = "`rr`Re`rd`x"
    SILVER = "`Ws`xi`Dlv`xe`Wr`x"
    CERULEAN = "`cc`Cer`cul`Cea`cn`x"
    YELLOW = "`yye`Yll`yow`x"
    PURPLE = "`013pu`005rp`013le`x"
    BLACK = "`240black`x"
    WHITE = "`Wwhite`x"


class Hair(Enum):
    """This enum is used to represent the available colors of a character's natural hair."""
    BLUE = "`cb`Clu`ce`x"
    BALD = "`wno`x"
    GREEN = "`gg`Gree`gn`x"
    PINK = "`Mpink`x"
    PUPRLE = "`mpurple`x"
    WHITE = "`Wwhite`x"
    BLACK = "`240black`x"
    BROWN = "`094brown`x"
    BLOND = "`179blond`x"
    AUBURN = "`130auburn`x"
    CHESTNUT = "`058chestnut`x"
    RED = "`166red`x"
    GRAY = "`243g`247ra`243y`x"


class Character(ObjectParent, DefaultCharacter):
    """
    The Character just re-implements some of the Object's methods and hooks
    to represent a Character entity in-game.

    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Object child classes like this.

    """

    MIN_FEET: int = 5
    MAX_FEET: int = 6
    MIN_INCHES: int = 0
    MAX_INCHES: int = 11

    def at_object_creation(self):
        super().at_object_creation()
        self.db.first_name = ""
        self.db.last_name = ""
        self.db.feet = 5
        self.db.inches = 7
        self.db.they = "they"
        self.db.them = "them"
        self.db.their = "their"
        self.db.hair = None
        self.db.eyes = None
        self.db.birth_month = 1
        self.db.birth_day = 1
        self.db.birth_year = 1980
        self.db.apparent_age = 45
        self.db.intro = "A newcomer"
