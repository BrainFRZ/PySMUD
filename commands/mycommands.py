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


class CmdHit(Command):
    """
    Hit a target.

    Usage:
      hit <target>

    """
    key = "hit"

    def parse(self):
        self.args = self.args.strip()
        target, *weapon = self.args.split(" with ", 1)
        if not weapon:
            target, *weapon = target.split(" ", 1)
        self.target = target.strip()
        if weapon:
            self.weapon = weapon[0].strip()
        else:
            self.weapon = ""

    def func(self):
        if not self.args:
            self.caller.msg("Who do you want to hit?")
            return
        # get the target for the hit
        target = self.caller.search(self.target)
        if not target:
            return
        # get and handle the weapon
        weapon = None
        if self.weapon:
            weapon = self.caller.search(self.weapon)
        if weapon:
            weapon_str = f"{weapon.key}"
        else:
            weapon_str = "bare fists"

        self.caller.msg(f"You hit {target.key} with {weapon_str}!")
        target.msg(f"You got hit by {self.caller.key} with {weapon_str}!")


class MyCmdSet(CmdSet):

    def at_cmdset_creation(self):
        self.add(CmdEcho)
