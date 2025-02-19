"""
A login menu using EvMenu.

Printer - February, 2025

Extending the contribution "menu_login" by Vincent-lg 2016, Griatch 2019 (rework for modern EvMenu)

This changes the Evennia login to ask for the account name and password in sequence instead of requiring you to enter
both at once. Once the account is logged in, the account details will be listed, including the roster of playable
characters. The player will then be able to 'quit' the game, choose which character to play, or 'create' a new one.

This uses Evennia's menu system EvMenu and is triggered by a command that is called automatically when a new user connects.
"""

from django.conf import settings

from evennia import CmdSet, Command, syscmdkeys
from evennia.utils.evmenu import EvMenu
from evennia.utils.utils import class_from_module

from server.conf.connection_screens import CONNECTION_SCREEN

_ACCOUNT = class_from_module(settings.BASE_ACCOUNT_TYPECLASS)

_ACCOUNT_HELP = "Enter a new or existing user name."
_PASSWORD_HELP = (
    "Password should be a minimum of 8 characters (preferably longer) and "
    "can contain a mix of letters, spaces, digits and @/./+/-/_/'/, only."
)


def _show_help(caller, raw_string, **kwargs):
    """Echo help message, then re-run node that triggered it"""
    help_entry = kwargs["help_entry"]
    caller.msg(help_entry)
    return None  # re-run calling node


def node_enter_username(caller, raw_text, **kwargs):
    """
    Ask for a user name. This is separated into its own node to allow for length validation to return without repeating
    the splash screen.
    """
    def _check_input(caller, username, **kwargs):
        """
        'Goto-callable', set up to be called from the _default option below.

        Called when user enters a username string. Check if this username already exists and set the
        flag 'new_user' if not. Will also directly login if the username is 'guest' and
        GUEST_ENABLED is True.

        The return from this goto-callable determines which node we go to next
        and what kwarg it will be called with.
        """
        username = username.rstrip("\n")
        if len(username) < 3:
            caller.msg("`xUsername must be at least 3 characters long.")
            return "node_enter_username"

        try:
            _ACCOUNT.objects.get(username__iexact=username)
        except _ACCOUNT.DoesNotExist:
            return "node_confirm_new_username", {"username": username}
        else:
            return "node_enter_password", {"username": username, "new_user": False}

    text = "`WWhat is your account name?"

    options = (
        {"key": "", "goto": "node_enter_username"},
        {"key": ("quit", "q"), "goto": "node_quit_or_login"},
        {"key": ("help", "h"), "goto": (_show_help, {"help_entry": _ACCOUNT_HELP, **kwargs})},
        {"key": "_default", "goto": _check_input},
    )
    return text, options

def node_confirm_new_username(caller, raw_text, **kwargs):
    """Handle confirmation for creating a new account."""

    username = kwargs.get("username", None)

    if not username:
        caller.msg("`RError: Missing required information for character creation!`x")
        return "node_character_selection", kwargs  # Redirect back

    text = "`xCreate a new account `c{}`x? (y/N)".format(username)
    options = (
        {"key": ("y", "yes"), "goto": ("node_enter_password", {"username": username, "new_user": True})},
        {"key": ("q", "quit"), "goto": "node_quit_or_login"},
        {"key": "_default", "goto": "node_enter_username"},
    )
    return text, options


def node_enter_password(caller, raw_string, **kwargs):
    """
    Handle password input.
    """
    def _check_input(caller, password, **kwargs):
        """
        'Goto-callable', set up to be called from the _default option below.

        Called when user enters a password string. Check username + password
        viability. If it passes, the account will have been created and login
        will be initiated.

        The return from this goto-callable determines which node we go to next
        and what kwarg it will be called with.
        """
        # these flags were set by the goto-callable
        username = kwargs["username"]
        new_user = kwargs["new_user"]
        password = password.rstrip("\n")

        session = caller
        address = session.address
        if new_user:
            # create a new account
            account, errors = _ACCOUNT.create(
                username=username, password=password, ip=address, session=session
            )
        else:
            # check password against existing account
            account, errors = _ACCOUNT.authenticate(
                username=username, password=password, ip=address, session=session
            )

        if account:
            if new_user:
                session.msg("`YA new account `c{}`Y was created. Welcome to the chaos!".format(username))
                return "node_quit_or_login", {"account": account, "login": True, "new_user": True}
            else:
                return "node_character_selection", {"account": account}
        else:
            # restart due to errors
            session.msg("`R{}".format("\n".join(errors)))
            kwargs["retry_password"] = True
            return "node_enter_password", kwargs

    def _restart_login(caller, *args, **kwargs):
        caller.msg("`xCancelled login.")
        return "node_enter_username"

    username = kwargs["username"]
    if kwargs["new_user"]:
        if kwargs.get("retry_password"):
            # Attempting to fix password
            text = "Enter a new password:"
        else:
            text = """
`cNotice`Y:`x SuperMUD is a mature role playing game in which there are few
restrictions on content. As such depictions of graphic violence or other mature
themes may be presented to the player over the course of their time here. By
continuing you state that you are not offended by mature material and that it
is legal for you to view it. If this is not the case please type '`cquit`x' now.

Type either `cquit`x or a new password for {}""".format(username)
    else:
        text = "Enter password (empty to abort):".format(username)

    options = (
        {"key": "", "goto": _restart_login},
        {"key": ("quit", "q"), "goto": "node_quit_or_login"},
        {"key": ("help", "h"), "goto": (_show_help, {"help_entry": _PASSWORD_HELP, **kwargs})},
        {"key": "_default", "goto": (_check_input, kwargs)}
    )
    return text, options

def node_character_selection(caller, raw_text, **kwargs):
    """Handle character selection. The list of the account's characters is displayed with details on each character."""
    def _check_input(caller, name, **kwargs):
        """
        'Goto-callable', set up to be called from the _default option below.

        Called when user enters a character name. Check to make sure the character entered is one of the avaialable
        characters playable with the account. If it passes, we initiate login.

        The return from this goto-callable determines whether we log in or try again
        """
        account = kwargs["account"]
        name = name.rstrip("\n").capitalize()
        if account.is_playable_name(name):
            return "node_quit_or_login", {"login": True, "account": account, "name": name}
        else:
            return None, {"account": account}

    account = kwargs["account"]

    options = (
        {"key": "", "goto": ("node_character_selection", kwargs)},
        {"key": "create", "goto": ("node_quit_or_login", {"login": True, "account": account})},
        {"key": ("quit", "q"), "goto": "node_quit_or_login"},
        {"key": "_default", "goto": (_check_input, kwargs)},
    )
    text = account.show_login_info()
    return text, options


def node_quit_or_login(caller, raw_text, **kwargs):
    """Exit menu, either by disconnecting or logging in."""
    session = caller
    if kwargs.get("login"):
        account = kwargs.get("account")
        name = kwargs.get("name")
        if not name:
            session.sessionhandler.login(session, account)
            new_user = kwargs.get("new_user")
            if not new_user:
                account.execute_cmd("create", session=session)
            return "", {}

        session.msg("`YLogging in ...`x")
        session.sessionhandler.login(session, account)
        account.execute_cmd(f"ic {name}", session=session)
    else:
        session.sessionhandler.disconnect(session, "Logging off. We hope to see you soon!")
    return "", {}


class MenuLoginEvMenu(EvMenu):
    """Version of EvMenu that does not display any of its options."""

    def node_formatter(self, nodetext, optionstext):
        return nodetext

    def options_formatter(self, optionlist):
        """Do not display the options, only the text.

        This function is used by EvMenu to format the text of nodes. The menu login
        is just a series of prompts so we disable all automatic display decoration
        and let the nodes handle everything on their own.
        """
        return ""


# Commands and CmdSets


class UnloggedinCmdSet(CmdSet):
    """Cmdset for the unloggedin state"""
    key = "DefaultUnloggedin"
    priority = 0

    def at_cmdset_creation(self):
        """Called when cmdset is first created."""
        self.add(CmdUnloggedinLook())


class CmdUnloggedinLook(Command):
    """
    An unloggedin version of the look command. This is called by the server
    when the account first connects. It sets up the menu before handing off
    to the menu's own look command.
    """

    key = syscmdkeys.CMD_LOGINSTART
    locks = "cmd:all()"
    arg_regex = r"^$"

    def func(self):
        self.caller.msg(CONNECTION_SCREEN)

        # Run the menu using the nodes in this module.
        menu_nodes = {
            "node_enter_username": node_enter_username,
            "node_confirm_new_username": node_confirm_new_username,
            "node_enter_password": node_enter_password,
            "node_character_selection": node_character_selection,
            "node_quit_or_login": node_quit_or_login
        }

        MenuLoginEvMenu(
            self.caller,
            menu_nodes,
            startnode="node_enter_username",
            auto_look=False,
            auto_quit=False,
            cmd_on_exit=None,
        )
