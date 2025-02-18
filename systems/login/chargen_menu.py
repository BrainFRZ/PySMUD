"""
EvMenu for Character Creation

Printer - February 2025
"""

import pendulum
from re import match as regex_match

from django.db.models import Q

from server.conf.settings import YEARS_IN_THE_FUTURE, TIMEZONE, MINIMUM_CHARACTER_AGE
from utils.string import listify
from typeclasses.characters import Character
from constants.character import (
    MIN_FEET, MAX_FEET,
    MIN_INCHES, MAX_INCHES,
    Eyes, Hair,
    Race
)


class ChargenData:
    """Stores the data for the character creation menu."""
    def __init__(self, caller):
        self.today = pendulum.today(tz=TIMEZONE)
        self.first_name, self.last_name = "NewCharacter", ""
        self.email = ""
        self.they, self.them, self.their = "they", "them", "their"
        self.race = Race.HUMAN
        self.tier = 1
        self.modifier = None
        self.birth_year, self.birth_month, self.birth_day = 1980, 1, 1
        self.feet, self.inches = 5, 7
        self.hair = None
        self.hairstyle = ""
        self.eyes = None
        self.trait = ""
        self.intro = "A newcomer"


def chargen_text(caller, data: ChargenData) -> str:
    """Displays the text for the character creation menu."""
    return f"""`cIn Character Creation`x

{show_name_lines(caller, data)}
Email`Y:`c {data.email}`x
Pronouns`Y:`c {data.they} {data.them} {data.their}`x
Race`Y: {str(data.race)}`x
Tier`Y:`c {data.tier}
Archetype`Y:`x {data.race.archetype(data.tier)} `Y(`xChange this with `cRace`x and `cTier`Y)`x
Modifiers`Y:`c {str(data.modifier or "")}`x
{get_birthday_line(data)}`x
Resulting Age`Y:`x {calculate_age(data)}`x
Feet`Y:`c {data.feet}`x
Inches`Y:`c {data.inches}`x
{show_part_line("Hair", data.hair)}`x
Hairstyle`Y:`x {data.hairstyle}`x
{show_part_line("Eyes", data.eyes)}`x
Trait`Y:`x {data.trait}`x
Intro`Y:`c {data.intro}`x

{karma_line(caller)}
{ready_line(caller, data)}
Syntax`Y:`c change `x(`cfield`x) (`cthing to change it to`x) or `chelp `x(`cfield`x)
"""


def node_chargen(caller, raw_string, **kwargs):
    """Manages the character creation menu and displays the text for the menu."""
    def _validate_and_update_name(field: str, name: str):
        """Validates and updates the first or last name entered by the user."""
        if len(data.first_name) < 2:
            caller.msg("First names must be at least two characters long.")
            return "node_chargen", {"data", data}
        if not name_validator(caller, data.first_name, data.last_name):
            caller.msg("Your first and last name can't match the first and last name of someone else. Also, your first name can't match one of someone else's codenames.")
            return "node_chargen", {"data", data}
        if field == "first_name":
            data.first_name = name
        elif field == "last_name":
            data.last_name = name
        else:
            raise ValueError(f"Invalid field name: {field}")
        return "node_chargen_end", {"data": data}


    def _validate_and_update_email(email: str):
        """Validates and updates the email entered by the user."""
        if not email_validator(email):
            caller.msg("Invalid email address.")
            return "node_chargen", {"data", data}
        data.email = email
        return "node_chargen", {"data", data}


    def _validate_and_update_pronouns(pronouns: str):
        """Validates and updates the pronouns entered by the user."""
        if not pronoun_validator(pronouns):
            caller.msg("Invalid pronouns. Please enter three distinct pronouns separated by spaces between two and ten characters long.")
            return "node_chargen", {"data", data}
        data.they, data.them, data.their = [pronoun.lower() for pronoun in pronouns.split()]
        return "node_chargen", {"data", data}


    def _validate_and_update_race(race: str):
        """Validates and updates the race entered by the user."""
        try:
            data.race = Race[race.upper()]
        except KeyError:
            caller.msg("Invalid race. Please see `chelp archetypes`x for a list of valid races.")
        return "node_chargen", {"data", data}


    def _validate_tier(tier: str):
        """Validates and updates the tier entered by the user."""
        try:
            tier_num = int(tier)
        except ValueError:
            caller.msg("Invalid tier. Please enter a number between 1 and 5.")
            return "node_chargen", {"data", data}
        if not data.race.valid_race_tier(tier_num):
            caller.msg("Invalid tier. Please see `chelp archetypes`x for a list of valid tiers for this race.")
            return "node_chargen", {"data", data}
        data.tier = tier_num
        return "node_chargen", {"data", data}


    def _validate_and_update_modifier(modifier: str):
        """Validates the modifier entered by the user.
        TODO: Create modifiers table"""
        pass


    def _validate_and_update_birthday(birthday_str: str):
        """Validates and updates the birthday entered by the user."""
        try:
            date = pendulum.from_format(birthday_str, "YYYY MM DD")
        except ValueError:
            caller.msg("Invalid birthday. Please enter a date in the format `cYYYY MM DD`x.")
            return "node_chargen", {"data", data}

        difference = data.today - date
        if difference.in_years() < MINIMUM_CHARACTER_AGE + YEARS_IN_THE_FUTURE:
            caller.msg(f"Your character must be at least {MINIMUM_CHARACTER_AGE} years old.")
            return "node_chargen", {"data", data}
        data.birth_month, data.birth_day, data.birth_year = date.month, date.day, date.year
        return "node_chargen", {"data", data}


    def _validate_and_update_height(height_type: str, height_str: str):
        """Validates and updates the feet or inches entered by the user."""
        try:
            height = int(height_str)
        except ValueError:
            caller.msg(f"Invalid {height_type}. Please enter a number between {MIN_FEET} and {MAX_FEET}.")
            return "node_chargen", {"data", data}

        if height_type == "feet":
            min_height, max_height = MIN_FEET, MAX_FEET
        elif height_type == "inches":
            min_height, max_height = MIN_INCHES, MAX_INCHES
        else:
            raise ValueError(f"Invalid height type: {height_type}")

        if height < min_height or height > max_height:
            caller.msg(f"Invalid feet. Please enter a number between {MIN_FEET} and {MAX_FEET}.")
            return "node_chargen", {"data", data}
        setattr(data, height_type, height)
        return "node_chargen", {"data", data}


    def _validate_and_update_part(part: str, color: str):
        """Validates and updates the hair or eyes color entered by the user."""
        if part == "hair":
            part_enum = Hair
        elif part == "eyes":
            part_enum = Eyes
        else:
            raise ValueError(f"Invalid part: {part}")

        try:
            part_obj = part_enum[color.upper()]
            setattr(data, part, part_obj)
        except KeyError:
            part_options = [str(part_obj) for part_obj in part_enum]
            caller.msg(f"Invalid {part} color. Valid colors: {listify(part_options)}")
        return "node_chargen", {"data", data}


    def _validate_and_update_text_field(field: str, txt: str):
        """Validates and udpates hairstyle, trait, and intro entered by the user."""
        if field not in {"hairstyle", "trait", "intro"}:
            raise ValueError(f"Invalid field name: {field}")

        if len(txt) < 5:
            caller.msg(f"{field.capitalize()} must be at least five characters long.")
            return "node_chargen", {"data", data}
        setattr(data, field, txt)
        return "node_chargen", {"data", data}


    def _handle_done():
        """Handles the `done` command."""
        if not is_ready(caller, data):
            return "node_chargen", {"data", data}
        else:
            return "node_chargen_end", {"data": data}


    data = kwargs.get("data", ChargenData(caller))
    text = chargen_text(caller, data)
    options = (
        {"key": ("first", "firstname"), "goto": _validate_and_update_name("first_name", **kwargs)},
        {"key": ("last", "lastname"), "goto": _validate_and_update_name("last_name", **kwargs)},
        {"key": "email", "goto": _validate_and_update_email(**kwargs)},
        {"key": "pronouns", "goto": _validate_and_update_pronouns(**kwargs)},
        {"key": "race", "goto": _validate_and_update_race(**kwargs)},
        {"key": "tier", "goto": _validate_tier(**kwargs)},
        {"key": "modifier", "goto": _validate_and_update_modifier(**kwargs)},
        {"key": "birthday", "goto": _validate_and_update_birthday(**kwargs)},
        {"key": "feet", "goto": _validate_and_update_height("feet", **kwargs)},
        {"key": "inches", "goto": _validate_and_update_height("inches", **kwargs)},
        {"key": "hair", "goto": _validate_and_update_part("hair", **kwargs)},
        {"key": "hairstyle", "goto": _validate_and_update_text_field(**kwargs)},
        {"key": "eyes", "goto": _validate_and_update_part("eyes", **kwargs)},
        {"key": "trait", "goto": _validate_and_update_text_field(**kwargs)},
        {"key": "intro", "goto": _validate_and_update_text_field(**kwargs)},
        {"key": "done", "goto": _handle_done()},
        {"key": ("quit", "q"), "goto": "node_quit"},
        {"key": "_default", "goto": ("node_chargen", {"data": data})},
    )
    return text, options


def node_chargen_end(caller, raw_string, **kwargs):
    data = kwargs["data"]
    caller.db.birth_year, caller.db.birth_month, caller.db.birth_day = data.birth_year, data.birth_month, data.birth_day
    caller.db.email = data.email
    caller.db.they, caller.db.them, caller.db.their = data.they, data.them, data.their
    caller.db.race = data.race
    caller.db.tier = data.tier
    caller.db.modifier = data.modifier
    caller.db.feet, caller.db.inches = data.feet, data.inches
    caller.db.hair = data.hair
    caller.db.hairstyle = data.hairstyle
    caller.db.eyes = data.eyes
    caller.db.trait = data.trait
    caller.db.intro = data.intro

    text = "Dust settles and your vision clears. With one `cLOOK`x, you know something has gone wrong."
    return text, None


def show_part_line(field: str, color: Hair | Eyes) -> str:
    """Highlights required fields if they are missing or invalid.
    :param field: Field name
    :param color: Enum color value for the field
    :return: The line as a string with the field highlighted red if the data is missing or invalid."""
    tag = f"`R{field}" if not color else field
    return f"{tag}`Y:`c {str(color or "")}`x"


def name_validator(caller, first_name: str, last_name: str) -> bool:
    """Validates the first or name entered by the user. The first name must be at least one character long.
    Written with assistance from Caracal Inspecter.
    :param caller: The character object.
    :param first_name: The character's first name.
    :param last_name: The character's last name.'
    :return: `True` if the first and last names are both valid, `False` otherwise"""
    first_name = caller.account.normalize_username(first_name)
    last_name = caller.account.normalize_username(last_name)

    # False if we're still on the default
    if first_name == "NewCharacter":
        return False

    # First name must be at least 3 letters and alphanumeric, while last name is optional and only needs to be alphanumeric
    if len(first_name) < 3 or (not first_name.isalnum()) or (last_name and not last_name.isalnum()):
        return False

    # Filter for first_name attribute, exact match, case insensitive
    first_name = Q(db_attributes__db_key="first_name", db_attributes__db_value__iexact=first_name)
    # Filter for last_name attribute, exact match, case insensitive
    last_name = Q(db_attributes__db_key="last_name", db_attributes__db_value__iexact=last_name)
    # Filter for first_name against first codename, exact match, case insensitive
    first_vs_code1 = Q(db_attributes__db_key="codename1", db_attributes__db_value__iexact=first_name)
    # Filter for first_name against second codename, exact match, case insensitive
    first_vs_code2 = Q(db_attributes__db_key="codename2", db_attributes__db_value__iexact=first_name)

    # now we actually do the checks!
    # NOTE: these will prevent conflicts with NPCs as well if they inherit from Character
    # We don't want two people with matching full names
    full_name = Character.objects.filter_family(first_name & last_name)

    # We don't want anyone's first name to match either of someone else's codenames
    codenames = Character.objects.filter_family(first_vs_code1 | first_vs_code2).distinct()

    return not (full_name or codenames)


def show_name_lines(caller, data: ChargenData) -> str:
    """Returns the lines with the first and last name of the character."""
    color = "" if name_validator(caller, data.first_name, data.last_name) else "`R"
    return f"{color}First Name`Y:`c {caller.db.first_name}`x\n{color}Last Name`Y:`c {caller.db.last_name}`x"


def email_validator(email: str) -> bool:
    """Validates the email entered by the user. The email must be a valid email address.
    :param email: The email entered by the user.
    :return: `True` if the email is a valid email address, `False` otherwise."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'
    return bool(regex_match(email_regex, email))


def pronoun_validator(pronouns: str) -> bool:
    """Validates the pronouns entered by the user. There must be three distinct pronouns separated by spaces, and each
    pronoun must be between two and ten characters long.
    :param pronouns: The list of pronouns entered by the user.
    :return: `True` if there are three distinct pronouns separated by spaces, False otherwise."""
    pronouns = pronouns.strip()
    pronoun_list = pronouns.split()
    return len(pronoun_list) != 3 and all(2 <= len(pronoun) <= 10 and pronoun.isalpha() for pronoun in pronoun_list)


def race_tier_modifier_validator(data: ChargenData) -> bool:
    """Validates the race, tier, and modifier are valid together. The race must be a valid Race enum value, and the tier
    must be valid for the given race. The modifier must also be valid for the resulting archetype.
    :param data: The data for the character creation menu.
    :return: `True` if the race, tier, and modifier are valid, `False` otherwise."""
    return data.race.valid_race_tier(data.tier)


def get_birthday_line(data: ChargenData) -> str:
    """Returns a line with the birthday of the character.
    TODO: Handle Synthetic maximum ages
    :param data: The data for the character creation menu.
    :return: A line with the birthday of the character."""
    month = data.birth_month
    day = data.birth_day
    year = data.birth_year
    try:
        date = pendulum.date(year, month, day)
        month_name, day_ord = date.format("MMMM Do").split()
    except ValueError:
        return f"`RBirthday`Y: `RInvalid birthday `Y[`xyyyy mm dd`Y]`x"

    return f"Birthday`Y:`x {year} {month} {day} `Y(`c{month_name} {day_ord}`Y,`c {year}`Y)[`xyyyy mm dd`Y]`x"


def calculate_age(data: ChargenData) -> int:
    """Calculates the age of the character based on their birthday.
    :param data: The data for the character creation menu.
    :return: The age of the character in years."""
    month = data.birth_month
    day = data.birth_day
    year = data.birth_year
    birthday = pendulum.datetime(year, month, day)
    difference = data.today - birthday
    return difference.in_years() + YEARS_IN_THE_FUTURE


def karma_line(caller) -> str:
    """Returns a line with the karma cost of making the character and how much karma the account currently has.
    Currently, all costs are 0.
    TODO: Implement karma system
    :param caller: The character object.
    :return: A line with the character's karma."""
    race = caller.db.race
    tier = caller.db.tier
    karma = caller.db.karma or 0
    cost = 0
    cost_color = "`R" if cost > 0 else "`G"
    return f"This character would cost {cost_color}{cost}`x karma to create, and you have `c{karma}`x karma."


def ready_line(caller, data: ChargenData) -> str:
    """Returns a line stating whether the character is ready to be created."""
    if is_ready(caller, data):
        return "This character is `Gready`x to be created! Type '`cdone`x' to proceed."
    else:
        return "This character is `Rnot yet ready`x to be created. Fields highlighted in `Rred`x must be filled."


def is_ready(caller, data: ChargenData) -> bool:
    """Returns whether the character is ready to be created."""
    cost = 0
    can_afford = cost <= caller.db.karma
    return (
        can_afford
        and name_validator(caller, data.first_name, data.last_name)
        and email_validator(data.email)
        and pronoun_validator(f"{data.they} {data.them} {data.their}")
        and race_tier_modifier_validator(data)
        and Hair.is_valid(data.hair) and Eyes.is_valid(data.eyes)
    )
