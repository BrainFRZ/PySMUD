from typeclasses.objects import Object

class Monster(Object):
    """
    This is a base class for Monsters.
    """
    def move_around(self):
        print(f"{self.key} is moving!")


class Dragon(Monster):
    """
    This is a dragon-specific Monster.
    """
    def at_object_creation(self):
        self.db.element = "fire"

    def move_around(self):
        super().move_around()
        print("The world trembles.")

    def breathe(self):
        """
        Let our dragon breathe their element.
        """
        print(f"{self.key} breathes {self.db.element}!")
