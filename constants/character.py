"""
Printer - February 2025

This file contains all the constants for a character.
"""

from enum import Enum

MIN_FEET: int = 5
MAX_FEET: int = 6
MIN_INCHES: int = 0
MAX_INCHES: int = 11


class Eyes(Enum):
    """This enum is used to represent the available colors of a character's eyes."""
    GOLDEN: str = "`Yg`yo`Yld`ye`Yn`x"
    AMBER: str = "`172am`166b`172er`x"
    BROWN: str = "`094br`yo`094wn`x"
    BLUE: str = "`027bl`026u`027e`x"
    GREEN: str = "`Ggr`ge`Gen`x"
    GRAY: str = "`243g`247ra`243y`x"
    HAZEL: str = "`028ha`058z`028el`x"
    RED: str = "`rr`Re`rd`x"
    SILVER: str = "`Ws`xi`Dlv`xe`Wr`x"
    CERULEAN: str = "`cc`Cer`cul`Cea`cn`x"
    YELLOW: str = "`yye`Yll`yow`x"
    PURPLE: str = "`013pu`005rp`013le`x"
    BLACK: str = "`240black`x"
    WHITE: str = "`Wwhite`x"

    @classmethod
    def is_valid(cls, color: str) -> bool:
        """Returns `True` if the given eye color is valid, `False` otherwise."""
        return color.upper() in (member.name for member in Eyes.__members__.values())


class Hair(Enum):
    """This enum is used to represent the available colors of a character's natural hair."""
    BLUE: str = "`cb`Clu`ce`x"
    BALD: str = "`wno`x"
    GREEN: str = "`gg`Gree`gn`x"
    PINK: str = "`Mpink`x"
    PURPLE: str = "`mpurple`x"
    WHITE: str = "`Wwhite`x"
    BLACK: str = "`240black`x"
    BROWN: str = "`094brown`x"
    BLOND: str = "`179blond`x"
    AUBURN: str = "`130auburn`x"
    CHESTNUT: str = "`058chestnut`x"
    RED: str = "`166red`x"
    GRAY: str = "`243g`247ra`243y`x"

    @classmethod
    def is_valid(cls, color: str) -> bool:
        """Returns `True` if the given hair color is valid, `False` otherwise."""
        return color.upper() in (member.name for member in Hair.__members__.values())


class Race(Enum):
    """This enum is used to represent the available races of a character."""
    HUMAN: str = "`cHuman`x"
    METAHUMAN: str = "`WMetahuman`x"
    MAGICKER: str = "`RMagicker`x"
    ALIEN: str = "`GAlien`x"
    SYNTHETIC: str = "`DSynthetic`x"
    AVALONIAN: str = "`CAvalonian`x"
    DIVER: str = "`YDiver`x"

    @classmethod
    def validate(cls, race: str):
        """Returns True if the given race is valid, False otherwise. Case insensitive."""
        special_names = {"META": Race.METAHUMAN, "SYNTH": Race.SYNTHETIC}
        race = race.upper()
        if race in (member.name for member in Race.__members__.values()):
            return Race[race.upper()]
        if race in special_names:
            return special_names[race]
        return None


    def race_tier_range(self) -> tuple[int, int]:
        """Returns a tuple containing the minimum and maximum tiers possible for this race."""
        match self:
            case Race.HUMAN:
                return 1, 5
            case Race.METAHUMAN:
                return 2, 5
            case Race.MAGICKER:
                return 2, 5
            case Race.ALIEN:
                return 2, 5
            case Race.SYNTHETIC:
                return 2, 5
            case Race.AVALONIAN:
                return 3, 5
            case Race.DIVER:
                return 3, 5
            case _:
                raise ValueError("Invalid race.")

    def valid_race_tier(self, tier: int) -> bool:
        """Returns `True` if the given tier is valid for this race, `False` otherwise."""
        return self.race_tier_range()[0] <= tier <= self.race_tier_range()[1]

    def archetype(self, tier: int, use_color: bool = True) -> str:
        """Returns a string representation of the race's tier archetype."""
        if not self.valid_race_tier(tier):
            raise ValueError(f"Invalid tier {tier} for race {self.name.capitalize()}.")
        match self:
            case Race.HUMAN:
                tiers = ["", "Bystander", "Regular Person", "Important Person", "Dedicated Human", "'Super'Human"]
                color = "`c"
            case Race.METAHUMAN:
                tiers = ["", "", "Rookie Metahuman", "Metahuman", "Veteran Metahuman", "S-Class Metahuman"]
                color = "`W"
            case Race.MAGICKER:
                tiers = ["", "", "Dabbler", "Practitioner", "Magician", "Supreme"]
                color = "`R"
            case Race.ALIEN:
                tiers = ["", "", "Rookie Alien", "Alien", "Veteran Alien", "Higher Lifeform"]
                color = "`G"
            case Race.SYNTHETIC:
                tiers = ["", "", "Prototype Synthetic", "Synthetic", "Advanced Synthetic", "Perfect Synthetic"]
                color = "`D"
            case Race.AVALONIAN:
                tiers = ["", "", "", "Avalonian", "Avalonian Knight", "Avalonian Noble"]
                color = "`C"
            case Race.DIVER:
                tiers = ["", "", "", "Diver", "Veteran Diver", "Elder Diver"]
                color = "`Y"
            case _:
                raise ValueError("Invalid race.")
        color = color if use_color else "`x"
        return f"{color}{tiers[tier]}`x"
