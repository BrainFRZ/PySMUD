"""
Character Creator contrib, by InspectorCaracal

Extended by Printer for SuperMUD, February 2025.

"""

import string
from random import choices

from django.conf import settings

from evennia import DefaultAccount
from evennia.commands.cmdset import CmdSet
from evennia.commands.default.account import CmdIC
from evennia.commands.default.muxcommand import MuxAccountCommand
from evennia.objects.models import ObjectDB
from evennia.utils.utils import string_partial_matching

from containers.RosterCharacterData import RosterCharacterData
from server.conf.settings import CHARGEN_MENU
from systems.login.chargen_menu import ChargenEvMenu

_MAX_NR_CHARACTERS = settings.MAX_NR_CHARACTERS

_CHARGEN_MENU = CHARGEN_MENU


class ContribCmdIC(CmdIC):
    def func(self):
        if self.args:
            # check if the args match an in-progress character
            wips = [chara for chara in self.account.characters if chara.db.chargen_step]
            if matches := string_partial_matching([c.key for c in wips], self.args):
                # the character is in progress, resume creation
                return self.execute_cmd("charcreate")
        super().func()


class ContribCmdCharCreate(MuxAccountCommand):
    """
    create a new character

    Begin creating a new character, or resume character creation for
    an existing in-progress character.

    You can stop character creation at any time and resume where
    you left off later.
    """

    key = "charcreate"
    aliases = ["create"]
    locks = "cmd:pperm(Player) and is_ooc()"
    help_category = "General"

    def func(self):
        """Create the new character"""
        account = self.account
        session = self.session

        # Only one character should be in progress at a time, so we check for WIPs first
        in_progress = [chara for chara in account.characters if chara.db.chargen_step]

        if len(in_progress):
            # We're continuing chargen for a WIP character
            new_character = in_progress[0]
        else:
            # Generate a randomized key so the player can choose a character name later
            key = "".join(choices(string.ascii_letters + string.digits, k=10))

            new_character, errors = account.create_character(
                key=key, location=None, ip=session.address
            )

            if errors:
                self.msg("\n".join(errors))
            if not new_character:
                return
            # Initalize the new character to the beginning of the chargen menu
            new_character.db.chargen_step = "node_chargen"
            # Make sure the character first logs in at the settings-defined start location
            new_character.db.prelogout_location = ObjectDB.objects.get_id(settings.START_LOCATION)

        # Set the menu node to start at to the character's last saved step
        startnode = new_character.db.chargen_step
        # Attach the character to the session, so the chargen menu can access it
        session.new_char = new_character

        # This gets called every time the player exits the chargen menu
        def finish_char_callback(session, menu):
            char = session.new_char
            if char.db.chargen_step:
                # This means the character creation process was exited in the middle
                account.execute_cmd("look", session=session)
            else:
                # Create a new roster entry for the account
                entry = RosterCharacterData()
                entry.name = char.db.first_name if not char.db.last_name else f"{char.db.first_name} {char.db.last_name}"
                entry.tier = char.db.tier
                entry.archetype = char.db.race.archetype(char.db.tier)
                entry.modifier = char.db.modifier
                account.db.roster.append(entry)

                # This means character creation was completed - start playing!
                # Execute the ic command to start puppeting the character
                account.execute_cmd("ic {}".format(char.key), session=session)

        ChargenEvMenu(session, _CHARGEN_MENU, startnode=startnode, cmd_on_exit=finish_char_callback)


class ContribChargenCmdSet(CmdSet):
    key = "Contrib Chargen CmdSet"

    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        self.add(ContribCmdIC)
        self.add(ContribCmdCharCreate)


class ContribChargenAccount(DefaultAccount):
    """
    A modified Account class that changes the OOC look output to better match the contrib and
    incorporate in-progress characters.
    """

    ooc_appearance_template = """
`Y--------------------------------------------------------------------`x
Welcome to `YSuperMUD`x! If this is your first time here, please type '`cstart`x' to get oriented.

You can use '`croster list`x' to see what pre-made characters might be available, or '`ccreate`x' if you want to create your own character.
`Y--------------------------------------------------------------------`x
""".strip()

    def at_look(self, target=None, session=None, **kwargs):
        """
        Called when this object executes a look. It allows to customize
        just what this means.

        Args:
            target (Object or list, optional): An object or a list
                objects to inspect. This is normally a list of characters.
            session (Session, optional): The session doing this look.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call (unused by default).

        Returns:
            look_string (str): A prepared look string, ready to send
                off to any recipient (usually to ourselves)

        """

        return self.ooc_appearance_template
