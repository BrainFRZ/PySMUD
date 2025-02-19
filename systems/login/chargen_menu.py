"""
EvMenu for Character Creation

Printer - February 2025
"""

import pendulum
from re import match as regex_match

from django.db.models import Q
from evennia.utils.evmenu import EvMenu

from server.conf.settings import YEARS_IN_THE_FUTURE, GAME_TIMEZONE, MINIMUM_CHARACTER_AGE
from utils.string import listify
from typeclasses.characters import Character
from constants.character import (
    MIN_FEET, MAX_FEET,
    MIN_INCHES, MAX_INCHES,
    Eyes, Hair,
    Race
)


DEFAULT_THEY, DEFAULT_THEM, DEFAULT_THEIR = "they", "them", "their"
DEFAULT_RACE = Race.HUMAN
DEFAULT_TIER = 1
DEFAULT_FEET, DEFAULT_INCHES = 5, 7
DEFAULT_BIRTH_YEAR, DEFAULT_BIRTH_MONTH, DEFAULT_BIRTH_DAY = 1980, 1, 1


class ChargenData:
    """Stores the data for the character creation menu."""

    def __init__(self):
        self.today = pendulum.today(tz=GAME_TIMEZONE)
        self.first_name, self.last_name = "NewCharacter", ""
        self.email = ""
        self.they, self.them, self.their = DEFAULT_THEY, DEFAULT_THEM, DEFAULT_THEIR
        self.race, self.tier, self.modifier = DEFAULT_RACE, DEFAULT_TIER, None
        self.birth_year, self.birth_month, self.birth_day = DEFAULT_BIRTH_YEAR, DEFAULT_BIRTH_MONTH, DEFAULT_BIRTH_DAY
        self.feet, self.inches = DEFAULT_FEET, DEFAULT_INCHES
        self.hair, self.eyes = None, None
        self.hairstyle = ""
        self.trait = ""
        self.intro = "A newcomer"


def chargen_text(caller, data: ChargenData) -> str:
    """Displays the text for the character creation menu."""
    return f"""`cIn Character Creation`x

{show_name_lines(caller, data)}
Email`Y:`c {data.email}`x
Pronouns`Y:`c {data.they} {data.them} {data.their}`x
Race`Y: {data.race.value}`x
Tier`Y:`c {data.tier}
Archetype`Y:`x {data.race.archetype(data.tier)} `Y(`xChange this with `cRace`x and `cTier`Y)`x
Modifiers`Y:`x None
{show_birthday_line(data)}`x
Resulting Age`Y:`x {calculate_age(data)}`x
Feet`Y:`c {data.feet}`x
Inches`Y:`c {data.inches}`x
{show_part_line("Hair", data.hair)}`x
Hairstyle`Y:`x {data.hairstyle}`x
{show_part_line("Eyes", data.eyes)}`x
Trait`Y:`x {data.trait}`x
Intro`Y:`c {data.intro}`x

{karma_line(caller, data)}
{ready_line(caller, data)}
Syntax`Y:`c change `x(`cfield`x) (`cthing to change it to`x) or `chelp `x(`cfield`x)
`x"""


def node_chargen(caller, raw_string, **kwargs):
    """Manages the character creation menu and displays the text for the menu."""

    def _validate_and_update_name(caller, field: str, name: str, **kwargs):
        """Validates and updates the first or last name entered by the user."""
        if field == "first_name":
            if len(name) < 2:
                caller.msg("First names must be at least two characters long.")
                return None, {"data": data}
            valid = name_validator(caller, name, data.last_name)
        elif field == "last_name":
            if not name:
                data.last_name = ""
                return None, {"data": data}
            elif len(name) < 2:
                caller.msg("Last names must be at least two characters long if you're using one.")
                return None, {"data": data}
            valid = name_validator(caller, data.first_name, name)
        else:
            raise ValueError(f"Invalid field name: {field}")

        if not valid:
            caller.msg("Your first and last name can't match the first and last name of someone else. Also, your first name can't match one of someone else's codenames.")
            return None, {"data": data}
        if field == "first_name":
            data.first_name = name
        elif field == "last_name":
            data.last_name = name
        else:
            raise ValueError(f"Invalid field name: {field}")
        return None, {"data": data}

    def _validate_and_update_email(caller, email: str, **kwargs):
        """Validates and updates the email entered by the user."""
        if not email_validator(email):
            caller.msg("Invalid email address.")
            return None, {"data": data}
        data.email = email
        return None, {"data": data}

    def _validate_and_update_pronouns(caller, pronouns: str, **kwargs):
        """Validates and updates the pronouns entered by the user."""
        if not pronoun_validator(pronouns):
            caller.msg("Invalid pronouns. Please enter three distinct pronouns separated by spaces between two and ten characters long.")
            return None, {"data": data}
        data.they, data.them, data.their = [pronoun.lower() for pronoun in pronouns.split()]
        return None, {"data": data}

    def _validate_and_update_race(caller, race: str, **kwargs):
        """Validates and updates the race entered by the user."""
        race_obj = Race.validate(race)
        if not race_obj:
            caller.msg("Invalid race. Please see `chelp archetypes`x for a list of valid races.")
            return None, {"data": data}
        data.race = race_obj

        # We want to bump the tier to the minimum possible if it's too low to avoid issues in the menu display for non-existing archetypes
        if not race_tier_modifier_validator(data):
            data.tier, _ = data.race.race_tier_range()

        return None, {"data": data}

    def _validate_tier(caller, tier_str: str, **kwargs):
        """Validates and updates the tier entered by the user."""
        try:
            tier = int(tier_str)
        except ValueError:
            caller.msg("Invalid tier. Please enter a number between 1 and 5.")
            return None, {"data": data}
        if not data.race.valid_race_tier(tier):
            min_tier, max_tier = data.race.race_tier_range()
            caller.msg(f"Invalid tier. Please enter a tier between {min_tier} and {max_tier}. See `chelp archetypes`x for more information on this race.")
            return None, {"data": data}
        data.tier = tier
        return None, {"data": data}

    def _validate_and_update_modifier(caller, modifier: str, **kwargs):
        """Validates the modifier entered by the user.
        TODO: Create modifiers table"""
        pass

    def _validate_and_update_birthday(caller, birthday_str: str, **kwargs):
        """Validates and updates the birthday entered by the user."""
        try:
            date = pendulum.from_format(birthday_str, "YYYY MM DD")
        except ValueError:
            caller.msg("Invalid birthday. Please enter a date in the format `cYYYY MM DD`x.")
            return None, {"data": data}

        difference = data.today - date
        if difference.in_years() < MINIMUM_CHARACTER_AGE + YEARS_IN_THE_FUTURE:
            caller.msg(f"Your character must be at least {MINIMUM_CHARACTER_AGE} years old.")
            return None, {"data": data}
        data.birth_month, data.birth_day, data.birth_year = date.month, date.day, date.year
        return None, {"data": data}

    def _validate_and_update_height(caller, height_type: str, height_str: str, **kwargs):
        """Validates and updates the feet or inches entered by the user."""
        try:
            height = int(height_str)
        except ValueError:
            caller.msg(f"Invalid {height_type}. Please enter a number between {MIN_FEET} and {MAX_FEET}.")
            return None, {"data": data}

        if height_type == "feet":
            min_height, max_height = MIN_FEET, MAX_FEET
        elif height_type == "inches":
            min_height, max_height = MIN_INCHES, MAX_INCHES
        else:
            raise ValueError(f"Invalid height type: {height_type}")

        if height < min_height or height > max_height:
            caller.msg(f"Invalid feet. Please enter a number between {MIN_FEET} and {MAX_FEET}.")
            return None, {"data": data}
        setattr(data, height_type, height)
        return None, {"data": data}

    def _validate_and_update_part(caller, part: str, color: str, **kwargs):
        """Validates and updates the hair or eyes color entered by the user."""
        if part == "hair":
            part_enum = Hair
        elif part == "eyes":
            part_enum = Eyes
        else:
            raise ValueError(f"Invalid part: {part}")

        if not part_enum.is_valid(color):
            part_options = [part_obj.value if part_obj != Hair.BALD else "`xbald" for part_obj in part_enum]
            caller.msg(f"Invalid {part} color. Valid colors: {listify(part_options)}")
            return None, {"data": data}
        part_obj = part_enum[color.upper()]
        setattr(data, part, part_obj)
        return None, {"data": data}

    def _validate_and_update_text_field(caller, field: str, txt: str):
        """Validates and udpates hairstyle, trait, and intro entered by the user."""
        if field not in {"hairstyle", "trait", "intro"}:
            raise ValueError(f"Invalid field name: {field}")

        if len(txt) < 5:
            caller.msg(f"{field.capitalize()} must be at least five characters long.")
            return None, {"data": data}
        setattr(data, field, txt)
        return None, {"data": data}

    def _handle_done(caller, raw_string, **kwargs):
        """Handles the `done` command."""
        data = kwargs["data"]
        if not is_ready(caller, data):
            if not name_validator(caller, data.first_name, data.last_name):
                caller.msg("Your first and last name can't match the first and last name of someone else. Also, your first name can't match one of someone else's codenames.")
            if not email_validator(data.email):
                caller.msg("Invalid email address.")
            if not pronoun_validator(f"{data.they} {data.them} {data.their}"):
                caller.msg(f"Invalid pronouns {data.they} {data.them} {data.their}. Please enter three distinct pronouns separated by spaces between two and ten characters long.")
            if not race_tier_modifier_validator(data):
                caller.msg(f"Invalid race and tier combination. Please see `chelp archetypes`x for a list of valid races and tiers.")
            if not data.hair or not data.eyes:
                caller.msg("Your hair and eyes must be valid colors.")
            if not intro_validator(data.intro):
                caller.msg("Your intro must be at least five characters long.")
            return None, {"data": data}
        else:
            return "node_chargen_end", {"data": data}

    def _parse_input(caller, raw_string, **kwargs):
        """Parses the CI option and input from the user."""
        input = raw_string.strip()
        data = kwargs.get("data", ChargenData())

        # Handle input for fields that clear with no argument
        clearable_fields = ["last", "lastname", "email", "hairstyle", "trait", "intro"]
        if input.lower() in clearable_fields:
            setattr(data, input.lower(), "")
            return None, {"data": data}

        listable_fields = {"hair": Hair, "eyes": Eyes, "race": Race}
        if input.lower() in listable_fields:
            part_enum = listable_fields[input.lower()]
            part_options = [part_obj.value if part_obj != Hair.BALD else "`xbald" for part_obj in part_enum]
            caller.msg(f"Valid {input} colors: {listify(part_options)}")
            return None, {"data": data}

        try:
            option, value = input.split(" ", 1)
        except ValueError:
            # No argument was given for an option that requires one
            return None, {"data": data}

        option = option.lower()
        if option == "first" or option == "firstname":
            return _validate_and_update_name(caller, "first_name", value, data=data)
        elif option == "last" or option == "lastname":
            return _validate_and_update_name(caller, "last_name", value, data=data)
        elif option == "email":
            return _validate_and_update_email(caller, value, data=data)
        elif option == "pronouns":
            return _validate_and_update_pronouns(caller, value, data=data)
        elif option == "race":
            return _validate_and_update_race(caller, value, data=data)
        elif option == "tier":
            return _validate_tier(caller, value, data=data)
        elif option == "birthday":
            return _validate_and_update_birthday(caller, value, data=data)
        elif option == "feet" or option == "inches":
            return _validate_and_update_height(caller, option, value, data=data)
        elif option == "hair" or option == "eyes":
            return _validate_and_update_part(caller, option, value, data=data)
        elif option == "hairstyle":
            return _validate_and_update_text_field(caller, "hairstyle", value)
        elif option == "trait":
            return _validate_and_update_text_field(caller, "trait", value)
        elif option == "intro":
            return _validate_and_update_text_field(caller, "intro", value)
        else:
            return None, {"data": data}

    data = kwargs.get("data", ChargenData())
    text = chargen_text(caller, data)
    options = (
        {"key": "", "goto": ("node_chargen", {"data": data})},
        {"key": ("quit", "q"), "goto": "node_quit"},
        {"key": "done", "goto": (_handle_done, kwargs)},
        {"key": "_default", "goto": (_parse_input, {"data": data})},
    )
    return text, options


def node_chargen_end(caller, raw_string, **kwargs):
    data = kwargs["data"]
    caller.new_char.key = f"{data.first_name}{data.last_name}"
    char_db = caller.new_char.db
    char_db.first_name, char_db.last_name = data.first_name, data.last_name
    char_db.birth_year, char_db.birth_month, char_db.birth_day = data.birth_year, data.birth_month, data.birth_day
    char_db.email = data.email
    char_db.they, char_db.them, char_db.their = data.they, data.them, data.their
    char_db.race = data.race
    char_db.tier = data.tier
    char_db.modifier = data.modifier
    char_db.feet, char_db.inches = data.feet, data.inches
    char_db.hair = data.hair
    char_db.hairstyle = data.hairstyle
    char_db.eyes = data.eyes
    char_db.trait = data.trait
    char_db.intro = data.intro

    caller.new_char.attributes.remove("chargen_step")

    text = "Dust settles and your vision clears. With one `cLOOK`x, you know something has gone wrong."
    return text, None


def node_quit(caller, raw_string, **kwargs):
    """Lets the user quit during chargen."""
    caller.sessionhandler.disconnect(caller, "Logging off. We hope to see you soon!")
    return "", {}


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

    # First name must be at least 2 letters and alphanumeric
    if len(first_name) < 2 or (not first_name.isalnum()):
        return False
    # If last name is given, it must be at least 2 letters and be alphanumeric
    if last_name and (not last_name.isalnum() or len(last_name) < 2):
        return False

    """
    # Filter for first_name attribute, exact match, case insensitive
    first_name = Q(db_attributes__db_key="first_name", db_attributes__db_value__iexact=first_name)
    # Filter for last_name attribute, exact match, case insensitive
    last_name = Q(db_attributes__db_key="last_name", db_attributes__db_value__iexact=last_name)
    # Filter for first_name against anyone else's first codename, exact match, case insensitive
    first_vs_code1 = Q(db_attributes__db_key="codename1", db_attributes__db_value__iexact=first_name)
    # Filter for first_name against anyone else's second codename, exact match, case insensitive
    first_vs_code2 = Q(db_attributes__db_key="codename2", db_attributes__db_value__iexact=first_name)

    # now we actually do the checks!
    # NOTE: these will prevent conflicts with NPCs as well if they inherit from Character
    # We don't want two people with matching full names
    full_name = Character.objects.filter_family(first_name & last_name)

    # We don't want anyone's first name to match either of someone else's codenames
    # In the future, this will use a GLOBAL_SCRIPT
    codenames = Character.objects.filter_family(first_vs_code1 | first_vs_code2)

    return not (full_name or codenames)
    """
    duplicate_names = [char for char in Character.objects.all()
        if char.db.first_name.lower() == first_name.lower() and char.db.last_name.lower() == last_name.lower()]
    duplicate_codenames = [char for char in Character.objects.all()
        if (char.db.codename1 and char.db.codename1.lower() == first_name.lower())
            or (char.db.codename2 and char.db.codename2.lower() == first_name.lower())]
    return not (duplicate_names or duplicate_codenames)

def email_validator(email: str) -> bool:
    """Validates the email entered by the user. The email must be a valid email address.
    :param email: The email entered by the user.
    :return: `True` if the email is a valid email address, `False` otherwise."""
    if not email:
        return True
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'
    return bool(regex_match(email_regex, email))


def pronoun_validator(pronouns: str) -> bool:
    """Validates the pronouns entered by the user. There must be three distinct pronouns separated by spaces, and each
    pronoun must be between two and ten characters long.
    :param pronouns: The list of pronouns entered by the user.
    :return: `True` if there are three distinct pronouns separated by spaces, False otherwise."""
    pronouns = pronouns.strip()
    pronoun_list = pronouns.split()
    return len(pronoun_list) == 3 and all(2 <= len(pronoun) <= 10 and pronoun.isalpha() for pronoun in pronoun_list)


def race_tier_modifier_validator(data: ChargenData) -> bool:
    """Validates the race, tier, and modifier are valid together. The race must be a valid Race enum value, and the tier
    must be valid for the given race. The modifier must also be valid for the resulting archetype.
    :param data: The data for the character creation menu.
    :return: `True` if the race, tier, and modifier are valid, `False` otherwise."""
    return data.race.valid_race_tier(data.tier)


def intro_validator(intro: str) -> bool:
    """Validates the intro entered by the user. The intro must be at least five characters long.
    :param intro: The intro entered by the user.
    :return: `True` if the intro is at least five characters long, `False` otherwise."""
    intro = intro.strip()
    return len(intro) >= 5


def show_name_lines(caller, data: ChargenData) -> str:
    """Returns the lines with the first and last name of the character."""
    color = "" if name_validator(caller, data.first_name, data.last_name) else "`R"
    return f"{color}First name`Y:`c {data.first_name}`x\n{color}Last name`Y:`c {data.last_name}`x"


def show_birthday_line(data: ChargenData) -> str:
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


def show_part_line(field: str, color: Hair | Eyes) -> str:
    """Highlights required fields if they are missing or invalid.
    :param field: Field name
    :param color: Enum color value for the field
    :return: The line as a string with the field highlighted red if the data is missing or invalid."""
    if not color:
        return f"`R{field}`Y:`x"
    return f"{field}`Y:`c {color.value}`x"


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


def karma_line(caller, data: ChargenData) -> str:
    """Returns a line with the karma cost of making the character and how much karma the account currently has.
    Currently, all costs are 0.
    TODO: Implement karma system
    :param caller: The character object.
    :param data: The data for the character creation menu.
    :return: A line with the character's karma."""
    race, tier = data.race, data.tier
    karma = caller.account.db.karma
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
    can_afford = cost <= caller.account.db.karma

    return (
        can_afford
        and name_validator(caller, data.first_name, data.last_name)
        and email_validator(data.email)
        and pronoun_validator(f"{data.they} {data.them} {data.their}")
        and race_tier_modifier_validator(data)
        and data.hair and data.eyes
        and intro_validator(data.intro)
    )


class ChargenEvMenu(EvMenu):
    """Version of EvMenu that does not display any of its options, copied from MenuLoginEvMenu"""

    def node_formatter(self, nodetext, optionstext):
        return nodetext

    def options_formatter(self, optionlist):
        """Do not display the options, only the text.

        This function is used by EvMenu to format the text of nodes. The menu login
        is just a series of prompts so we disable all automatic display decoration
        and let the nodes handle everything on their own.
        """
        return ""
