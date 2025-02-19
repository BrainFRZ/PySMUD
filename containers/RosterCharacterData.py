class RosterCharacterData:
    """
    This container class is used to store data about a character in an account's roster. It is used to display an
    accounts list of characters during login.
    """
    def __init__(self):
        self.name = ""
        self.tier = 1
        self.archetype = None
        self.modifier = None


    def __str__(self):
        tier_colors = ["", "`c", "`C", "`Y", "`p", "`M"]

        if self.archetype and self.modifier:
            return f"`W{self.name.strip()}`Y: `xTier {tier_colors[self.tier]}{self.tier}`x {self.archetype} `Y(`x{self.modifier}`Y)`x"
        elif self.archetype:
            return f"`W{self.name.strip()}`Y: `xTier {tier_colors[self.tier]}{self.tier}`x {self.archetype}`x"
        else:
            return f"`W{self.name}`x"
