from business.exceptions import LevelUpException 
class XpHandler:
    def __init__(self, level: int, current_xp : int):
        self.level = level
        self.current_xp = current_xp
        self.xp_to_next_level = self.calculate_xp_for_next_level()

    def calculate_xp_for_next_level(self):
        """Calculates the XP required for the next level."""
        if self.level == 1:
            return 5
        elif 2 <= self.level <= 20:
            return 5 + 10 * (self.level - 1)
        elif 21 <= self.level <= 40:
            return 5 + 10 * 19 + 13 * (self.level - 20)
        elif self.level > 40:
            return 5 + 10 * 19 + 13 * 20 + 16 * (self.level - 40)

    def add_xp(self, xp: int):
        """Add XP and check for level up."""
        self.current_xp += xp
        while self.current_xp >= self.xp_to_next_level:
            self.level_up()

    def level_up(self):
        """Level up the player."""
        self.current_xp -= self.xp_to_next_level
        self.level += 1
        self.xp_to_next_level = self.calculate_xp_for_next_level()
        raise LevelUpException

    def get_level(self):
        """Get the current level of the player."""
        return self.level

    def get_current_xp(self):
        """Get the current XP the player has."""
        return self.current_xp

    def get_xp_for_next_level(self):
        """Get the XP required for the next level."""
        return self.xp_to_next_level
