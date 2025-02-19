"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

from evennia.objects.objects import DefaultCharacter

from .objects import ObjectParent


class Character(ObjectParent, DefaultCharacter):
    """
    The Character just re-implements some of the Object's methods and hooks
    to represent a Character entity in-game.

    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Object child classes like this.

    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.first_name = "New"
        self.db.last_name = "Character"
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
        self.db.race = None
        self.db.codename1 = ""
        self.db.codename2 = ""
