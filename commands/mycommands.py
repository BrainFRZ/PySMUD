from commands.command import Command
from evennia import CmdSet


class CmdEcho(Command):
    """
    A simple echo command

    Usage:
        echo <something>

    """
    key = "echo"

    def func(self):
        self.caller.msg(f"Echo: '{self.args}'")


class MyCmdSet(CmdSet):

    def at_cmdset_creation(self):
        self.add(CmdEcho)
